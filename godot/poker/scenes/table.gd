extends Node2D

# Precargamos la escena de la carta visual
var card_scene: PackedScene = preload("res://scenes/Card.tscn")

# 1. Cambiamos Control por Node2D
@onready var player_hand_container: Node2D = $PlayerHand
@onready var deck_position: Marker2D = $DeckPosition
@onready var discard_position: Marker2D = $DiscardPosition
@onready var game_manager: GameManager = GameManager.new()
@onready var pause_button: Button = $UI/PauseBtn
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
	pause_button.pressed.connect(_on_pause_button_pressed)

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
	# ¡Que empiece el juego automático!
	# (El _ready de game_manager disparará change_state(START_GAME))

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
		# Modo Dios: pasamos true para ver todas las cartas
		render_hand(config["hand"], p.hand_cards, true, config["vertical"])

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

func render_player_hand(player: Player):
	var p_index = game_manager.players.find(player)
	var config = hand_containers[p_index]
	render_hand(config["hand"], player.hand_cards, true, config["vertical"])

# Renderiza la mano de un jugador específico
func render_hand(container: Node2D, cards: Array[Card], is_face_up: bool, is_vertical: bool = false) -> void:
	# Limpiar cartas visuales anteriores
	for child in container.get_children():
		child.queue_free()
		
	var index: int = 0
	var spacing: float = 10 # Cartas de bots más apretadas/compactas
	
	for c_data in cards:
		var card_view: CardView = card_scene.instantiate()
		container.add_child(card_view)
		
		if is_vertical:
			card_view.position = Vector2(0, (index * spacing) - 50)
		else:
			card_view.position = Vector2((index * spacing) - 40, 0)
			
		card_view.setup(c_data, is_face_up)
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
