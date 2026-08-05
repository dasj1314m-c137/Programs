extends RefCounted

class_name Card

var suit: String
var value: int
var face_down: bool = true
var discarded: bool = false

func _init(a_suit: String, a_value: int):
	suit = a_suit
	value = a_value
	
func get_name() -> String:
	return str(value) + " of " + suit
