cociente = (input("Ingrese el numero y te daremos su secuencia: "))

negativo = False
secuencia_bits = []

if "-" in cociente:
    cociente = cociente.replace("-", "")
    negativo = True

cociente = int(cociente)

while cociente != 0:
    bit_residuo = cociente % 2
    secuencia_bits.append(str(bit_residuo))
    cociente = cociente // 2

if len(secuencia_bits) < 8:
    for i in range(8-len(secuencia_bits)):
        secuencia_bits.append("0")

if negativo:
     for i in range(2):
        for j in range(8):
            if secuencia_bits[j] == "1":
                secuencia_bits[j] = "0"
            else:         
                secuencia_bits[j] = "1"
                if i == 1:
                    break

secuencia_bits = "".join(reversed(secuencia_bits))

print(f"Esta es la secuencia de bits {secuencia_bits}")