class_name GameManager
extends Node

# --- SEÑALES PARA LA INTERFAZ VISUAL ---
signal state_changed(new_state: State)
signal cards_dealt(players: Array[Player])
signal card_drawn(card: Card)
signal card_discarded(card: Card, face_up: bool)
signal turn_changed(current_player: Player)
signal melds_updated(player: Player, melds: Array[Array])
signal render_player_hand(player: Player)
signal human_hand_interaction(player: Player, phase: HumanPhase)
signal human_action_done
signal human_claim_resolved(took: bool)

enum State {
	START_GAME,
	START_ROUND,
	DEAL_CARDS,
	PLAYER_TURN,
	CHECK_DISCARD_CLAIM,
	EVALUATE,
	END_ROUND
}

enum HumanPhase {
	NONE,
	MELD,
	DISCARD
}

var current_state: State
var deck: Deck
var players: Array[Player] = []
var last_discarded_card: Card
var card_to_discard: Card
var meld_discard: bool = false
var winner: Player = null
var current_player_index: int = 0
var is_forced_turn: bool = false
var is_discarded_turn: bool = false
var is_claim_turn: bool = false
var back_card: Card = Card.new("diamond", 1)

func _ready() -> void:
	# Iniciamos la máquina de estados
	change_state(State.START_GAME)

func change_state(new_state: State) -> void:
	current_state = new_state
	state_changed.emit(current_state)
	
	match current_state:
		State.START_GAME:
			_setup_game()
		State.START_ROUND:
			_setup_round()
		State.DEAL_CARDS:
			_deal_cards()
		State.PLAYER_TURN:
			_start_player_turn()
		State.CHECK_DISCARD_CLAIM:
			check_who_claims_card()
		State.EVALUATE:
			_evaluate_winner()
		State.END_ROUND:
			_end_round()

# --- MÉTODOS PRIVADOS DE CADA ESTADO ---

func _setup_game() -> void:
	deck = Deck.new()
	# Un jugador humano (is_bot = false) + 3 bots
	players.append(Player.new("Jugador", false))
	players.append(Player.new("Bot 1"))
	players.append(Player.new("Bot 2"))
	players.append(Player.new("Bot 3"))
	
	change_state(State.START_ROUND)

func _setup_round() -> void:
	deck.gen_deck()
	deck.shuffle_deck()
	
	# El humano siempre queda en la posición 0 (abajo) y los bots se barajan
	var human: Player = null
	var bots: Array[Player] = []
	for player in players:
		if player.is_bot:
			bots.append(player)
		else:
			human = player
	bots.shuffle()
	players.clear()
	if human != null:
		players.append(human)
	for bot in bots:
		players.append(bot)
	
	for player in players:
		player.clear_hand()
		player.took_discarded = false
	
	# print("--- NUEVA RONDA INICIADA ---")
	change_state(State.DEAL_CARDS)

func _deal_cards() -> void:
	# Se reparten 9 cartas a cada jugador según tus reglas
	for i in range(9):
		for player in players:
			player.save_card(deck.deal_card())
	
	# print("9 cartas repartidas a cada jugador con éxito.")
	cards_dealt.emit(players) # <-- Avisamos a Table.gd
	await get_tree().create_timer(1.0, false).timeout
	
	# Transición al primer turno de la partida
	current_player_index = 0
	change_state(State.PLAYER_TURN)

func _start_player_turn() -> void:
	var active_player = players[current_player_index]
	turn_changed.emit(active_player)
	# print("\n>>> Turno de: ", active_player.name)
	# Aquí el juego se detiene a esperar que el jugador o la IA realice su acción

	# Turno humano: detenemos la máquina de estados esperando su interacción
	if not active_player.is_bot:
		await _run_human_turn(active_player)
		return

	await get_tree().create_timer(0.8, false).timeout
# --- ACCIONES DURANTE LA PARTIDA ---
	if is_forced_turn:
		is_forced_turn = false # Reseteamos la bandera
		# print(active_player.name, " debe pagar por la carta que tomó forzada.")
		card_discarded.emit(back_card, false)
		melds_updated.emit(active_player, active_player.melds_down)
		await get_tree().create_timer(1.0, false).timeout
		
		# Intenta bajar otras cosas si le quedaron combinaciones
		active_player.try_down_melds()
		if active_player.melds_changed:
			active_player.melds_changed = false
			melds_updated.emit(active_player, active_player.melds_down)
			await get_tree().create_timer(1.0, false).timeout
			
		# ¿El jugador ganó al bajar? (10+ cartas bajadas)
		if Evaluator.has_won(active_player.melds_down):
			_declare_winner(active_player)
			return
			
		# Paga descartando una carta de su mano
		card_to_discard = active_player.choose_card_to_discard()
		if card_to_discard:
			player_discards_card(active_player, card_to_discard)
		return
		
	if is_discarded_turn:
		is_discarded_turn = false
		# El bot pudo tomar la carta solo para formar un par: baja solo si tiene jugada completa
		if meld_discard:
			meld_discard = false
			active_player.down_melds()
			render_player_hand.emit(active_player)
			await get_tree().create_timer(0.2, false).timeout
			melds_updated.emit(active_player, active_player.melds_down)
			await get_tree().create_timer(1.0, false).timeout
		
			# ¿El jugador ganó al bajar? (10+ cartas bajadas)
			if Evaluator.has_won(active_player.melds_down):
				_declare_winner(active_player)
				return
				
			# print(active_player.name, " debe pagar por la carta descartada que tomo.")
			# Paga descartando una carta de su mano
			card_to_discard = active_player.choose_card_to_discard()
			if card_to_discard:
				player_discards_card(active_player, card_to_discard)
			return
		
		else:
			card_to_discard = Evaluator.card_to_discard
			Evaluator.card_to_discard = null
			if card_to_discard:
				player_discards_card(active_player, card_to_discard)
			return


	# 1. El jugador roba una carta del mazo
	var drawn_card = deck.deal_card()
	if drawn_card == null:
		# print("¡El mazo se ha quedado sin cartas! Fin de la partida.")
		change_state(State.EVALUATE)
		return
	
	active_player.save_card(drawn_card)
	card_drawn.emit(drawn_card)
	# print(active_player.name, " robó del mazo: ", drawn_card.get_name())
	
	await get_tree().create_timer(1.0, false).timeout
	# 2. Revisa si puede bajar alguna jugada a la mesa
	active_player.try_down_melds()
	if active_player.melds_changed:
		active_player.melds_changed = false
		render_player_hand.emit(active_player)
		await get_tree().create_timer(0.2, false).timeout
		melds_updated.emit(active_player, active_player.melds_down)
		await get_tree().create_timer(1.0, false).timeout
	
	if drawn_card in active_player.hand_cards:
		if active_player.can_down_meld(drawn_card):
			active_player.remove_card(drawn_card)
			render_player_hand.emit(active_player)
			await get_tree().create_timer(0.2, false).timeout
			melds_updated.emit(active_player, active_player.melds_down)
			await get_tree().create_timer(1.0, false).timeout
		

	# ¿El jugador ganó al bajar? (10+ cartas bajadas)
	if Evaluator.has_won(active_player.melds_down):
		_declare_winner(active_player)
		return

	# 3. Elige una carta y la paga/descarta		
	card_to_discard = active_player.choose_card_to_discard()
	if card_to_discard:
		player_discards_card(active_player, card_to_discard)

func _run_human_turn(player: Player) -> void:
	# Turno forzado: la carta entró en sus bajadas, solo debe pagar descartando
	if is_forced_turn:
		is_forced_turn = false
		# print(player.name, " debe pagar por la carta que tomó forzada.")
		card_discarded.emit(back_card, false)
		melds_updated.emit(player, player.melds_down)
		await get_tree().create_timer(0.6, false).timeout
		if Evaluator.has_won(player.melds_down):
			_declare_winner(player)
			return
		await _human_discard_phase(player)
		return
		
	# Turno de carta tomada del pozo: la bajada ya se hizo al aceptar la carta,
	# así que solo queda pagar descartando
	if is_discarded_turn:
		is_discarded_turn = false
		render_player_hand.emit(player)
		if Evaluator.has_won(player.melds_down):
			_declare_winner(player)
			return
		await _human_discard_phase(player)
		return
		
	# Turno normal: roba automáticamente del mazo
	var drawn_card = deck.deal_card()
	if drawn_card == null:
		# print("¡El mazo se ha quedado sin cartas! Fin de la partida.")
		change_state(State.EVALUATE)
		return
	
	player.save_card(drawn_card)
	card_drawn.emit(drawn_card)
	# print(player.name, " robó del mazo: ", drawn_card.get_name())
	await get_tree().create_timer(1.0, false).timeout
	
	# El humano decide qué jugadas bajar con el botón "Bajar jugada"
	if player.hand_cards.size() > 3 or player.has_play():
		await _human_meld_phase(player)
	
	if Evaluator.has_won(player.melds_down):
		_declare_winner(player)
		return
	
	await _human_discard_phase(player)

func _human_meld_phase(player: Player) -> void:
	human_hand_interaction.emit(player, HumanPhase.MELD)
	await human_action_done

func _human_discard_phase(player: Player) -> void:
	human_hand_interaction.emit(player, HumanPhase.DISCARD)
	await human_action_done

# --- MÉTODOS LLAMADOS DESDE LA UI (jugador humano) ---

# Baja las cartas seleccionadas si forman una jugada válida.
func human_down_meld(player_index: int, selected: Array[Card]) -> bool:
	var player = players[player_index]
	if player.is_bot or not player.down_selected_meld(selected):
		return false
	render_player_hand.emit(player)
	melds_updated.emit(player, player.melds_down)
	return true

# El humano terminó de bajar jugadas (botón "Pasar").
func human_finish_meld_phase() -> void:
	human_action_done.emit()

# El humano eligió qué carta descartar.
func human_discard(player_index: int, card: Card) -> void:
	var player = players[player_index]
	if player.hand_cards.has(card):
		player_discards_card(player, card)
	human_action_done.emit()

# El humano respondió si toma o no la carta del pozo.
func respond_claim(took: bool) -> void:
	human_claim_resolved.emit(took)

func player_discards_card(player: Player, card: Card) -> void:
	# print(player.name, " descartó: ", card.get_name())
	last_discarded_card = card
	last_discarded_card.discarded = true
	player.remove_card(card)
	render_player_hand.emit(player)
	await get_tree().create_timer(0.3, false).timeout
	
	card_discarded.emit(card, true)
	await get_tree().create_timer(1.0, false).timeout
	
	# Pasamos a comprobar si alguien está obligado por sus cartas bajadas
	change_state(State.CHECK_DISCARD_CLAIM)

func check_who_claims_card() -> void:
	var total_players = players.size()
	var claimed: bool = false
	
	# Buscamos en orden de cercanía (sentido horario) desde el siguiente jugador
	for i in range(1, total_players):
		var check_index = (current_player_index + i) % total_players
		var candidate_player = players[check_index]
		
		# Verifica únicamente cartas bajadas públicas
		if candidate_player.can_down_meld(last_discarded_card):
			# print("¡ROBO FORZADO! A ", candidate_player.name, " le entra la carta en sus bajadas.")
			# print("El turno SALTA a ", candidate_player.name)
			
			current_player_index = check_index
			claimed = true
			candidate_player.took_discarded = true
			
			# Transición de turno para que el jugador obligado pague descartando otra
			# ¡AQUÍ MARCAMOS QUE ES UN TURNO FORZADO!
			is_forced_turn = true
			change_state(State.PLAYER_TURN)
			break
			
	if not claimed:
		for i in range(1, total_players):
			var check_index = (current_player_index + i) % total_players
			var candidate_player = players[check_index]
			
			if not candidate_player.took_discarded:
				candidate_player.save_card(last_discarded_card)
				card_discarded.emit(back_card, false)
				card_drawn.emit(last_discarded_card)
				await get_tree().create_timer(1.0, false).timeout
				
				var should_claim: bool = false
				if candidate_player.is_bot:
					if candidate_player.has_play() and candidate_player.is_discarded_play():
						should_claim = true
						meld_discard = true
					elif Evaluator.is_discard_useful(candidate_player.hand_cards, last_discarded_card):
						should_claim = true
						print(candidate_player.name, " va a usar la carta descartada: ", last_discarded_card.get_name())
				else:
					if candidate_player.took_discarded:
						# Ya tomó un descarte en esta cadena: pasa automáticamente
						should_claim = false
					else:
						# Entregamos la carta y mostramos la UI normal de bajar/pasar.
						# Pasar = devolver la carta; bajar una jugada = tomar la carta.
						is_claim_turn = true
						human_hand_interaction.emit(candidate_player, HumanPhase.MELD)
						should_claim = await human_claim_resolved
						is_claim_turn = false
				
				if should_claim:
					last_discarded_card.discarded = false
					current_player_index = check_index
					claimed = true
					candidate_player.took_discarded = true
					
					is_discarded_turn = true
					change_state(State.PLAYER_TURN)
					break
			
				candidate_player.remove_card(last_discarded_card)
				card_drawn.emit(last_discarded_card)
				card_discarded.emit(last_discarded_card, true)
				await get_tree().create_timer(1.0, false).timeout
				
	if not claimed:
		# Fin de la cadena de reclamos: se resetean las banderas de descarte tomado
		for player in players:
			player.took_discarded = false
		print("Nadie estuvo obligado a tomar la carta. Cae al pozo de descarte.")
		_advance_turn_normal()

func _advance_turn_normal() -> void:
	current_player_index = (current_player_index + 1) % players.size()
	change_state(State.PLAYER_TURN)

func _declare_winner(player: Player) -> void:
	winner = player
	# Re-render de la última jugada bajada antes de terminar
	melds_updated.emit(player, player.melds_down)
	# print("\n*** ¡", player.name, " HA GANADO! ***")
	change_state(State.EVALUATE)

func _evaluate_winner() -> void:
	# print("--- EVALUANDO GANADOR ---")
	if winner == null:
		# Fallback: si el mazo se agotó, buscamos quién llegó a 10 cartas
		for player in players:
			if Evaluator.has_won(player.melds_down):
				winner = player
				break
	if winner != null:
		print("Ganador: ", winner.name, " con ", Evaluator.count_melded_cards(winner.melds_down), " cartas bajadas.")
		melds_updated.emit(winner, winner.melds_down)
	else:
		print("No hay ganador.")
	change_state(State.END_ROUND)

func _end_round() -> void:
	if winner != null:
		print("Ronda finalizada. ¡", winner.name, " gana la partida!")
	else:
		print("Ronda finalizada sin ganador.\n")
