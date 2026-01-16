userOpr = input("Que operacion quieres obtener su resultado en secuencia de 8 bits: ")

resta = False
preNegative = False
oprs = ["-", "+"]


if "-" in userOpr:
    resta = True
    if "+" in userOpr and userOpr[0] == "-":
        preNegative = True

for opr in oprs:
    userOpr = userOpr.replace(opr, " ")

nums = [int(x) for x in userOpr.split()]

if preNegative:
    rdo = nums[1] - nums[0]
elif resta:
    rdo = nums[0] - nums[1]
else:
    rdo = nums[0] + nums[1]

negativo = False
secuencia_bits = []
cociente = str(rdo)

if "-" in cociente:
    cociente = cociente.replace("-", "")
    negativo = True

cociente = int(cociente)

while cociente != 0:
    bit_residuo = cociente % 2
    secuencia_bits.append(str(bit_residuo))
    cociente = cociente // 2

while len(secuencia_bits) < 8:
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

secuencia = "".join(reversed(secuencia_bits))

print(f"Esta es la secuencia de bits {secuencia}")