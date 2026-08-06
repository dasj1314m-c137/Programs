class_name Evaluator
extends RefCounted

static func num_group(cards: Array[Card]):
	if cards.size() < 3:
		return false
	var value = cards[0].value
	for card in cards:
		if card.value != value:
			return false
	return true
	
static func straight(cards: Array[Card]):
	if cards.size() < 3:
		return false
	var suit = cards[0].suit
	
	for card in cards:
		if card.suit != suit:
			return false
	var cards_copy: Array[Card] = cards.duplicate()
	cards_copy.sort_custom(func(a: Card, b: Card): return a.value < b.value)
	
	for i in range(cards_copy.size()):
		if i > 0:
			if cards_copy[i].value != cards_copy[i - 1].value + 1:
				return false
	
	return true

static func check_play(cards: Array[Card]) -> bool:
	return num_group(cards) or straight(cards)
		
static func can_add_to_meld(meld: Array[Card], card: Card):
	var tmp_meld: Array[Card] = []
	for c in meld:
		tmp_meld.append(c)
	tmp_meld.append(card)
	
	return check_play(tmp_meld)

# --- HEURÍSTICA DE EVALUACIÓN DE MANO ---

# Evalúa una mano y devuelve su puntaje total (float).
# Las jugadas completas se extraen primero (mayor prioridad) y sus cartas
# quedan "aisladas" en `used` para que no se reutilicen en proyectos incompletos.
static func evaluate_hand(hand: Array[Card]) -> float:
	# 1. Clonamos las referencias para no alterar el array original ni los objetos Card.
	var cards: Array[Card] = []
	for card in hand:
		cards.append(card)

	var used: Array[Card] = []
	var score := 0.0

	# --- 2. JUGADAS COMPLETAS (prioridad máxima) ---
	score += _extract_tercias(cards, used)
	score += _extract_escaleras(cards, used)

	# --- 3. JUGADAS INCOMPLETAS / PROYECTOS (solo con cartas sobrantes) ---
	score += _extract_pares(cards, used)
	score += _extract_escaleras_seguidas(cards, used)
	score += _extract_escaleras_hueco(cards, used)

	# --- 4. PENALIZACIÓN DE CARTAS SOBRANTES ---
	for card in cards:
		if used.has(card):
			continue
		if _es_aislada(card, cards):
			score -= float(card.value)   # Carta inservible: penaliza su valor alto
		else:
			score -= 10.0                # Carta duplicada/redundante que rompe fluidez

	return score

# Marca 3 cartas del mismo valor como usadas y devuelve +200 por cada tercia.
static func _extract_tercias(cards: Array[Card], used: Array[Card]) -> float:
	var gained := 0.0
	var by_value: Dictionary = {}
	for card in cards:
		if not by_value.has(card.value):
			by_value[card.value] = []
		by_value[card.value].append(card)

	for value in by_value:
		var group: Array = by_value[value]
		while group.size() >= 3:
			gained += 200.0
			for i in 3:
				used.append(group.pop_back())
	return gained

# Detecta escaleras completas (3+ cartas consecutivas del mismo palo).
# Devuelve +200 base (+50 extra por cada carta adicional tras la 3ra).
static func _extract_escaleras(cards: Array[Card], used: Array[Card]) -> float:
	var gained := 0.0
	var by_suit: Dictionary = {}
	for card in cards:
		if not by_suit.has(card.suit):
			by_suit[card.suit] = []
		by_suit[card.suit].append(card)

	for suit in by_suit:
		var suit_cards: Array[Card] = _unused_of(cards, by_suit[suit], used)
		suit_cards.sort_custom(func(a: Card, b: Card): return a.value < b.value)

		var values: Array[int] = []
		for card in suit_cards:
			if not values.has(card.value):
				values.append(card.value)
		values.sort()

		# Recorremos valores consecutivos formando "runs" de escalera completa.
		var run: Array[int] = []
		for value in values:
			if run.is_empty() or value == run[-1] + 1:
				run.append(value)
			else:
				gained += _score_run(run, suit_cards, used)
				run = [value]
		gained += _score_run(run, suit_cards, used)
	return gained

# Si el run tiene 3+ valores consecutivos, marca una carta por valor como usada
# y devuelve los puntos ganados por esa escalera completa.
static func _score_run(run: Array[int], suit_cards: Array[Card], used: Array[Card]) -> float:
	if run.size() < 3:
		return 0.0
	var gained := 200.0 + float(run.size() - 3) * 50.0
	for value in run:
		for card in suit_cards:
			if card.value == value and not used.has(card):
				used.append(card)
				break
	return gained

# Busca pares (2 cartas del mismo valor) entre las cartas no usadas: +50 por par.
static func _extract_pares(cards: Array[Card], used: Array[Card]) -> float:
	var gained := 0.0
	var by_value: Dictionary = {}
	for card in cards:
		if used.has(card):
			continue
		if not by_value.has(card.value):
			by_value[card.value] = []
		by_value[card.value].append(card)

	for value in by_value:
		var group: Array = by_value[value]
		while group.size() >= 2:
			gained += 50.0
			used.append(group.pop_back())
			used.append(group.pop_back())
	return gained

# Busca escaleras seguidas (2 cartas consecutivas del mismo palo): +35.
static func _extract_escaleras_seguidas(cards: Array[Card], used: Array[Card]) -> float:
	var gained := 0.0
	var by_suit: Dictionary = {}
	for card in cards:
		if not by_suit.has(card.suit):
			by_suit[card.suit] = []
		by_suit[card.suit].append(card)

	for suit in by_suit:
		var suit_cards: Array[Card] = _unused_of(cards, by_suit[suit], used)
		var values: Array[int] = []
		for card in suit_cards:
			if not values.has(card.value):
				values.append(card.value)
		values.sort()

		for i in range(values.size() - 1):
			if values[i + 1] != values[i] + 1:
				continue
			var first := _card_with_value(values[i], suit_cards, used)
			var second := _card_with_value(values[i + 1], suit_cards, used)
			if first != null and second != null:
				used.append(first)
				used.append(second)
				gained += 35.0
	return gained

# Busca escaleras con hueco (2 cartas del mismo palo con distancia 2): +15.
static func _extract_escaleras_hueco(cards: Array[Card], used: Array[Card]) -> float:
	var gained := 0.0
	var by_suit: Dictionary = {}
	for card in cards:
		if not by_suit.has(card.suit):
			by_suit[card.suit] = []
		by_suit[card.suit].append(card)

	for suit in by_suit:
		var suit_cards: Array[Card] = _unused_of(cards, by_suit[suit], used)
		var values: Array[int] = []
		for card in suit_cards:
			if not values.has(card.value):
				values.append(card.value)
		values.sort()

		for i in range(values.size()):
			for j in range(i + 1, values.size()):
				if values[j] != values[i] + 2:
					continue
				var first := _card_with_value(values[i], suit_cards, used)
				var second := _card_with_value(values[j], suit_cards, used)
				if first != null and second != null:
					used.append(first)
					used.append(second)
					gained += 15.0
	return gained

# Devuelve una carta no usada de un valor dado dentro del array de cartas del palo.
static func _card_with_value(value: int, suit_cards: Array[Card], used: Array[Card]) -> Card:
	for card in suit_cards:
		if card.value == value and not used.has(card):
			return card
	return null

# Determina si una carta está aislada: sin igual valor ni vecino de palo a distancia <= 2.
static func _es_aislada(card: Card, cards: Array[Card]) -> bool:
	for other in cards:
		if other == card:
			continue
		if other.value == card.value:
			return false
		if other.suit == card.suit and abs(other.value - card.value) <= 2:
			return false
	return true

# Devuelve la sublista de cartas de un palo que aún no están marcadas como usadas.
static func _unused_of(_all_cards: Array[Card], suit_cards: Array, used: Array[Card]) -> Array[Card]:
	var result: Array[Card] = []
	for card in suit_cards:
		if not used.has(card):
			result.append(card)
	return result

# --- DECISIÓN DE DESCARTE (Greedy Search) ---

# Recibe la mano tras robar (N+1 cartas) y devuelve la carta cuyo descarte
# deja la mano mejor evaluada. No modifica el array original ni las cartas.
static func choose_card_to_discard(hand_with_draw: Array[Card]) -> Card:
	var best_card_to_discard: Card = null
	var max_score := -999999.0

	for card in hand_with_draw:
		# Copia superficial de la mano omitiendo únicamente la carta actual.
		var temp_hand: Array[Card] = []
		for c in hand_with_draw:
			if c != card:
				temp_hand.append(c)

		var score := evaluate_hand(temp_hand)
		if score > max_score:
			max_score = score
			best_card_to_discard = card

	return best_card_to_discard

# --- DECISIÓN DE TOMAR CARTA DESCARTADA (Bots) ---

# Mejora mínima para que un bot tome una carta descartada. Con 35 cubre el par
# (+50) y las 2 seguidas del mismo palo (+35); NO cubre los huecos (+15).
const DISCARD_CLAIM_THRESHOLD: float = 35.0
# Recibe la mano YA con la carta descartada incluida. Compara la mejor mano
# posible (quedándose el descarte y soltando la peor carta) contra su mano sin
# esa carta. Devuelve true si la mejora alcanza el umbral.
static func is_discard_useful(hand_with_discard: Array[Card], discarded: Card) -> bool:
	var base_hand: Array[Card] = []
	for c in hand_with_discard:
		if c != discarded:
			base_hand.append(c)
	var base_score := evaluate_hand(base_hand)

	var to_discard := choose_card_to_discard(hand_with_discard)
	if to_discard == null:
		return false
	var temp_hand := hand_with_discard.duplicate()
	temp_hand.erase(to_discard)
	var improved_score := evaluate_hand(temp_hand)

	return improved_score - base_score >= DISCARD_CLAIM_THRESHOLD
	
# --- DETECCIÓN DE GANADOR ---

# Suma el total de cartas bajadas por un jugador (tamaño de todas sus jugadas).
static func count_melded_cards(melds_down: Array[Array]) -> int:
	var total := 0
	for meld in melds_down:
		total += meld.size()
	return total

# Un jugador gana cuando ha bajado 10 o más cartas (sin importar cuántas jugadas).
static func has_won(melds_down: Array[Array]) -> bool:
	return count_melded_cards(melds_down) >= 10
