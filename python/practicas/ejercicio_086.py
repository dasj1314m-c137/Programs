from math import log

# exponente_log = log(5**2)
# bajamos_exponente = 2 * log(5)

# division_log = log(5 / 2)
# bajamos_division = log(5) - log(2)

# print(f"Exponente en logaritmo {exponente_log}, exponente bajado {bajamos_exponente}")
# print(f"Divison en logaritmo {division_log} division bajado {bajamos_division}")

start_amount = float(input("Ingresa la cantidad incial (C): "))
end_amount = float(input("Ingresa la cantidad final (C'): "))
tasa_interes = float(input("Ingresa la tasa de interes: "))

# partimos de esta formula C' = C * (1 + x / 100)**n que calcula la capital final con interes compuesto dato un interes y capital inicial
# primero dejamos solo la operacion con n (el numero de años) para eso movemos la cantidad inicial y lo pasamos dividiendo
# C' / C = (1 + x / 100)**n
# luego lo que debemos hacer es bajar el exponente y para hacerlo usamos logaritmos como mostramos arriba y se pasa multiplicando p.j:
# C' / C = n * log(1 + x / 100)
# y como aplicamos logaritmos de un lado tenemos que hacerlo del otro lado para mantener la igualdad
# log(C' / C) = n * log(1 + x / 100)
# para no hacer la division en el logaritmo podemos bajar la division y hacer resta
# log(C') - log(C) = n * log(1 + x / 100)
# ahora como ultimo paso debemos pasar el lado que no tiene la incognita a despejar osea log(C') - log(C) ya que queremos despejar n
# y entonces lo pasamos y n lo pasamos del otro lado, pero como es multiplicacion ahora es division porque se paso
# n = (log(C') - log(C)) / log(1 + x / 100)
# ponemos parentesis alrededor de (log(C') - log(C)) para que se resten y no dividan antes log(C) el orden importa checa eso

n = (log(end_amount) - log(start_amount)) / log(1 + tasa_interes / 100)

print(
    f"Para que {start_amount} llegue a {end_amount} a un crecimiento anual del {tasa_interes}% deben pasar: {round(n, 4)} años"
)
