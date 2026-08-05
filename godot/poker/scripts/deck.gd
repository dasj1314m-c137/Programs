extends RefCounted

class_name Deck

var deck: Array[Card] = []
var suits: Array[String] = ["hearts", "diamonds", "spades", "clubs"]

func _init():
	gen_deck()
	
func gen_deck():
	deck.clear()
	for suit in suits:
		for i in range(13):
			deck.append(Card.new(suit, i+1))

func shuffle_deck():
	deck.shuffle()
	
func deal_card():
	if not deck.is_empty():
		return deck.pop_back()
