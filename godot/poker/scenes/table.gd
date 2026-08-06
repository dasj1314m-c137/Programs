extends Node2D

# Precargamos la escena de la carta visual
var card_scene: PackedScene = preload("res://scenes/Card.tscn")

# game_player = true  → oculta las manos de los bots (modo real)
# game_player = false → god mode: todas las cartas visibles (para pruebas)
var game_player: bool = true

# Estado de interacción del jugador humano (MELD / DISCARD)
var interaction_phase: int = GameManager.HumanPhase.NONE
var interaction_player_index: int = -1
var selected_cards: Array[CardView] = []

@onready var player_hand_container: Node2D = $PlayerHand
@onready var deck_position: Marker2D = $DeckPosition
@onready var discard_position: Marker2D = $DiscardPosition
@onready var game_manager: GameManager = GameManager.new()
@onready var pause_button: Button = $UI/PauseBtn
@onready var turn_label: Label = $UI/TurnLabel
@onready var play_button: Button = $UI/PlayBtn
@onready var pass_button: Button = $UI/PassBtn
@onready var reject_button: Button = $UI/RejectBtn
# Guardamos la relación entre la posición del jugador y su nodo visual
@onready var hand_containers = {
	0: {"hand": $PlayerHand, "plays": $PlayerPlays, "vertical": false},
	1: {"hand": $Bot1Hand,   "plays": $Bot1Plays,   "vertical": true},
	2: {"hand": $Bot2Hand,   "plays": $Bot2Plays,   "vertical": false},
	3: {"hand": $Bot3Hand,   "plays": $Bot3Plays,   "vertical": true}
}

func _ready() -> void:
	# Configura el modo de proceso para que se detenga cuando el juego entre en pausa
	game_manager.process_mode = Node.PROCESS_MODE_PAUSABLE
	add_child(game_manager) # Agregamos la lógica al árbol
	
	# Conectamos las señales del GameManager a nuestras funciones visuales
	game_manager.render_player_hand.connect(render_player_hand)
	game_manager.cards_dealt.connect(_on_cards_dealt)
	game_manager.card_drawn.connect(_on_card_drawn)
	game_manager.card_discarded.connect(_on_card_discarded)
	game_manager.melds_updated.connect(_on_melds_updated)
	game_manager.human_hand_interaction.connect(_on_human_hand_interaction)
	game_manager.human_action_done.connect(_on_human_action_done)
	pause_button.pressed.connect(_on_pause_button_pressed)
	play_button.pressed.connect(_on_play_button_pressed)
	pass_button.pressed.connect(_on_pass_button_pressed)
	reject_button.pressed.connect(_on_reject_button_pressed)
	
	_hide_action_buttons()

func _on_pause_button_pressed() -> void:
	# Invertimos el estado actual de pausa del juego
	var is_paused: bool = not get_tree().paused
	get_tree().paused = is_paused
	
	# Cambiamos el texto del botón para retroalimentación visual
	if is_paused:
		pause_button.text = "Reanudar ▶️"
		print("--- SIMULACIÓN EN PAUSA ---")
	else:
		pause_button.text = "Pausar ⏸️"
		print("--- SIMULACIÓN REANUDADA ---")

func _on_melds_updated(player: Player, melds: Array[Array]) -> void:
	var p_index = game_manager.players.find(player)
	if p_index != -1:
		var config = hand_containers[p_index]
		render_melds(config["plays"], melds, config["vertical"])

func _on_cards_dealt(players: Array[Player]) -> void:
	update_all_hands(players)

func _on_card_drawn(_card: Card) -> void:
	update_all_hands(game_manager.players)

func _on_card_discarded(card: Card, face_up: bool) -> void:
	update_discard_pile_view(card, face_up) # Muestra la carta en el pozo
	update_all_hands(game_manager.players)

func update_all_hands(players: Array[Player]) -> void:
	for i in range(players.size()):
		var p = players[i]
		var config = hand_containers[i]
		# game_player = true → solo la mano del humano se ve boca arriba
		var face_up: bool = (not p.is_bot) or (not game_player)
		var spacing: float = 10
		render_hand(config["hand"], p.hand_cards, face_up, config["vertical"], spacing)

# Muestra la última carta del pozo de descarte en su Marker2D
func update_discard_pile_view(top_card_data: Card, face_up: bool) -> void:
	# Limpiamos la carta anterior del pozo si existe
	for child in discard_position.get_children():
		child.queue_free()
		
	if top_card_data != null:
		var card_view: CardView = card_scene.instantiate()
		discard_position.add_child(card_view)
		card_view.position = Vector2.ZERO
		card_view.setup(top_card_data, face_up)

func render_player_hand(player: Player) -> void:
	var p_index = game_manager.players.find(player)
	var config = hand_containers[p_index]
	var face_up: bool = (not player.is_bot) or (not game_player)
	render_hand(config["hand"], player.hand_cards, face_up, config["vertical"])

# Renderiza la mano de un jugador específico
func render_hand(container: Node2D, cards: Array[Card], is_face_up: bool, is_vertical: bool = false, spacing: float = 10) -> void:
	# Limpiar cartas visuales anteriores
	for child in container.get_children():
		child.queue_free()
		
	var index: int = 0
	
	for c_data in cards:
		var card_view: CardView = card_scene.instantiate()
		container.add_child(card_view)
		
		if is_vertical:
			card_view.position = Vector2(0, (index * spacing) - 50)
		else:
			card_view.position = Vector2((index * spacing) - 40, 0)
			
		if c_data.discarded:
			is_face_up = true
		card_view.setup(c_data, is_face_up)
		card_view.clicked.connect(_on_card_clicked)
		index += 1

# Renderiza un conjunto de combinaciones (melds) bajadas por un jugador
func render_melds(container: Node2D, melds: Array[Array], is_vertical: bool = false) -> void:
	# Limpiamos bajadas previas del nodo
	for child in container.get_children():
		child.queue_free()

	var current_offset: float = 0
	var card_spacing: float = 10  # Pegaditas dentro de la misma jugada
	var meld_gap: float = 10     # Separación entre una jugada y otra

	for meld in melds: # 'meld' es un Array[Card] que representa 1 tercia o corrida
		for c_data in meld:
			var card_view: CardView = card_scene.instantiate()
			container.add_child(card_view)
			
			# Posicionamos según la orientación (horizontal o vertical)
			if is_vertical:
				card_view.position = Vector2(0, current_offset - 50)
			else:
				card_view.position = Vector2(current_offset - 40, 0)
			
			card_view.setup(c_data, true) # Las bajadas SIEMPRE se ven boca arriba
			# Avanzamos el offset corto para la siguiente carta de la MISMA jugada
			current_offset += card_spacing
			
		# Al terminar una jugada completa, sumamos el espacio EXTRA para la siguiente
		current_offset += meld_gap

# --- INTERACCIÓN DEL JUGADOR HUMANO ---

func _on_human_hand_interaction(player: Player, phase: int) -> void:
	_hide_action_buttons()
	interaction_phase = phase
	interaction_player_index = game_manager.players.find(player)
	selected_cards.clear()
	
	var config = hand_containers[interaction_player_index]
	render_hand(config["hand"], player.hand_cards, true, config["vertical"])
	
	turn_label.visible = true
	if phase == GameManager.HumanPhase.MELD:
		if game_manager.is_claim_turn:
			turn_label.text = "Te entregaron una carta del pozo: 'Bajar jugada', 'Pasar', 'Rechazar'"
		else:
			turn_label.text = "Tu turno: selecciona 3-4 cartas y presiona 'Bajar jugada'."
		play_button.visible = true
		pass_button.visible = true
		reject_button.visible = game_manager.is_claim_turn
	elif phase == GameManager.HumanPhase.DISCARD:
		turn_label.text = "Tu turno: haz clic en la carta que quieras descartar."

func _on_human_action_done() -> void:
	interaction_phase = GameManager.HumanPhase.NONE
	_hide_action_buttons()

func _on_card_clicked(card_view: CardView) -> void:
	if interaction_phase == GameManager.HumanPhase.NONE:
		return
	var active_player = game_manager.players[interaction_player_index]
	if active_player.is_bot:
		return
	if card_view.get_parent() != hand_containers[interaction_player_index]["hand"]:
		return
	
	if interaction_phase == GameManager.HumanPhase.DISCARD:
		game_manager.human_discard(interaction_player_index, card_view.card_data)
	elif interaction_phase == GameManager.HumanPhase.MELD:
		_toggle_selection(card_view)

func _toggle_selection(card_view: CardView) -> void:
	if card_view.selected:
		card_view.set_selected(false)
		selected_cards.erase(card_view)
	elif selected_cards.size() < 5:
		card_view.set_selected(true)
		selected_cards.append(card_view)

func _on_play_button_pressed() -> void:
	if selected_cards.size() < 3:
		turn_label.text = "Selecciona al menos 3 cartas."
		return
	var cards: Array[Card] = []
	for cv in selected_cards:
		cards.append(cv.card_data)
	if game_manager.human_down_meld(interaction_player_index, cards):
		# Solo se puede bajar UNA jugada por turno → pasar directo al descarte
		if game_manager.is_claim_turn:
			_respond_claim(true)
		else:
			game_manager.human_finish_meld_phase()
	else:
		turn_label.text = "Esa combinación no es válida. Elige otra."

func _on_pass_button_pressed() -> void:
	if interaction_phase == GameManager.HumanPhase.MELD:
		game_manager.players[interaction_player_index].play.clear()
		if game_manager.is_claim_turn:
			_respond_claim(true)
		else:
			game_manager.human_finish_meld_phase()

func _on_reject_button_pressed() -> void:
	if interaction_phase == GameManager.HumanPhase.MELD and game_manager.is_claim_turn:
		game_manager.players[interaction_player_index].play.clear()
		_respond_claim(false)

func _respond_claim(value: bool) -> void:
	selected_cards.clear()
	interaction_phase = GameManager.HumanPhase.NONE
	_hide_action_buttons()
	game_manager.respond_claim(value)

func _hide_action_buttons() -> void:
	turn_label.visible = false
	play_button.visible = false
	pass_button.visible = false
	reject_button.visible = false
