print("Este programa suma dos secuencias binarias que le pases acontinuacion")

seq1 = input("Ingresa la primera sequencia binaria: ")
seq2 = input("Ingresa la segunda secuencia binaria: ")

rdo_sum = 0

sequences = [seq1, seq2]

for seq in sequences:
    for i, bit in enumerate(reversed(seq)):
        if bit == "1":
            value_posicional = 2**i
            rdo_sum += value_posicional

print(f"El resultado de la suma de ambas secuencias binarias es: {rdo_sum}")