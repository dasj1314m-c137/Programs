extends RefCounted

class_name Player

var name: String
var hand_cards: Array[Card] = []
var melds_down: Array[Array]
var melds_changed: bool = false
var play: Array[Card]
var is_bot: bool = true
var took_discarded: bool = false

func _init(a_name: String, bot: bool = true):
	name = a_name
	is_bot = bot
	
func save_card(a_card: Card):
	hand_cards.append(a_card)
	
func remove_card(card: Card):
	hand_cards.erase(card)

func clear_hand():
	hand_cards.clear()
	melds_down.clear()
	
func can_down_meld(discarded_card):
	for meld in melds_down:
		if Evaluator.can_add_to_meld(meld, discarded_card):
			meld.append(discarded_card)
			meld.sort_custom(func(a, b): return a.value < b.value)
			return true
	return false

func is_discarded_play():
	return play.any(func(card): return card.discarded)

# El bot decide qué carta descartar usando la heurística Greedy del Evaluator.
func choose_card_to_discard() -> Card:
	return Evaluator.choose_card_to_discard(hand_cards)

# Intenta buscar entre sus cartas si tiene alguna tercia o escalera para bajar a la mesa
func try_down_melds() -> void:
	play.clear()
	# Revisa combinaciones de 3 cartas en su mano
	if play or has_play():
		melds_changed = true
		down_melds()
	return

func down_melds():
	print("--> ¡", name, " BAJÓ UNA COMBINACIÓN A LA MESA! <--")
	play.sort_custom(func(a, b): return a.value < b.value)
	melds_down.append(play.duplicate())

	# Removemos las cartas de la mano
	print("¡BAJO LAS CARTAS!")
	for card in play:
		print(card.get_name())
		hand_cards.erase(card)
	play.clear()
	return

# El humano selecciona 3-4 cartas y el botón "Bajar jugada" valida con el Evaluator.
func down_selected_meld(selected: Array[Card]) -> bool:
	if not Evaluator.check_play(selected):
		return false
	selected.sort_custom(func(a, b): return a.value < b.value)
	melds_down.append(selected.duplicate())
	for card in selected:
		hand_cards.erase(card)
	melds_changed = true
	return true
	
func has_play():
	if hand_cards.size() < 3:
		return
	# Revisa combinaciones de 3 cartas en su mano
	for i in range(hand_cards.size()):
		for j in range(i + 1, hand_cards.size()):
			for k in range(j + 1, hand_cards.size()):
				var comb: Array[Card] = [hand_cards[i], hand_cards[j], hand_cards[k]]
				if Evaluator.check_play(comb):
					play = comb
					return true
	return false
