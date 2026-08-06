extends Area2D
class_name CardView

signal clicked(card_view: CardView)

@onready var face_sprite: Sprite2D = $FaceSprite
@onready var back_sprite: Sprite2D = $BackSprite

var card_data: Card
var is_face_up: bool = true
var selected: bool = false

func _ready() -> void:
	input_event.connect(_on_input_event)

func _on_input_event(_viewport: Node, event: InputEvent, _shape_idx: int) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		clicked.emit(self)

func setup(a_card_data: Card, start_face_up: bool = true) -> void:
	card_data = a_card_data
	is_face_up = start_face_up
	
	if start_face_up:
		_load_face_texture()
	set_face_up(is_face_up)

func set_selected(value: bool) -> void:
	selected = value
	if selected:
		position.y -= 12
		z_index = 2
	else:
		position.y += 12
		z_index = 1

func _load_face_texture() -> void:
	if card_data == null:
		return
		
	# Convertimos el valor numérico (1..13) al sufijo del archivo de tu pack
	var value_str: String = ""
	match card_data.value:
		1: value_str = "A"
		11: value_str = "J"
		12: value_str = "Q"
		13: value_str = "K"
		_:
			# Agrega un cero a la izquierda para 2..9 (ej. 2 -> "02", 10 -> "10")
			value_str = "%02d" % card_data.value

	# Armamos la ruta exacta: res://assets/cards/card_hearts_05.png
	var path: String = "res://assets/cards/card_%s_%s.png" % [card_data.suit, value_str]
	
	if ResourceLoader.exists(path):
		face_sprite.texture = load(path)
	else:
		push_error("¡No se encontró la imagen!: " + path)

func set_face_up(show_front: bool) -> void:
	is_face_up = show_front
	face_sprite.visible = show_front
	back_sprite.visible = not show_front
