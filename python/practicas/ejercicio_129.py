# en este programa vamos a calcula el MCD (minimo comun divisor) el divisor mas grande
# para eso usaremos el algoritmo de Euclides el cual se basa en la siguiente regla matematica
# Si un numero 'd' divide a dos numeros 'a' y 'b', tambien divide a su diferencia '-' y su resto 'r'

# Si 'd' divide a '(a, b)' → 'd' también divide a '(b, r)'
# Si 'd' divide a '(b, r)' → 'd' también divide a '(a, b)'
# por lo tanto los divisores comunes de 'a', 'b' y 'r' son los mismos

# entonces el algoritmo de Euclides se basa en lo siguiente:
# 1er paso: dividir el numero mayor entre el menor obteniendo el resto osea 'a % b'
# 2do paso: el valor de 'b' se pasa a 'a' osea 'a = b' y el valor de 'r' se pasa a 'b'
# 3er paso: repetir proceso hasta que el resto sea 0
# 4to paso: cuando el resto sea 0 el divisor actual '(b)' sera el MCD

# porque esto funciona? porque como dijimos anteriormente "los divisores comunes de 'a', 'b' y 'r' son los mismos"
# entonces cuando el resto sea 0 significa que encontramos el MCD de 'a', 'b' y 'r', y el MCD es el divisor actual '(b)'

a = int(input("Ingresa el numero mayor: "))
b = int(input("Ingresa el numero menor: "))

while True:
    resto = a % b
    if (resto != 0):
        a = b
        b = resto
        continue
    break

print(f"El MCD (minimo comun divisor) es: {b}")
