import math
from collections import Counter

def rango(lista):
    return max(lista) - min(lista)

def varianza(lista):
    med = media(lista)
    suma = 0
    for i in lista:
        suma += (i - med)**2
    return suma / len(lista)

def desviacion_estandar(lista):
    desviacion = math.sqrt(varianza(lista))
    return round(desviacion, 2)

def mediana(lista):
    n = len(lista)
    sorted_list = sorted(lista)
    mid = n // 2
    if n % 2 == 0:
        med = (sorted_list[mid - 1] + sorted_list[mid]) / 2
    else:
        med = sorted_list[mid]
    return med

def media(lista):
    return round(sum(lista) / len(lista), 2)

def moda(lista):
    frequencyA = frecA(lista)
    max_freq = max(frequencyA.values())
    modes = [str(key) for key, value in frequencyA.items() if value == max_freq]
    if len(modes) == len(frequencyA):
        return None
    return " , ".join(modes)

def calcular_frecAcum(dic_frecA):
    frecuenciaAcum = 0
    for item in dic_frecA:
        frecuenciaAcum += dic_frecA[item]
        dic_frecA[item] = frecuenciaAcum
    return dic_frecA

def calcular_frecR(dic_frecA):
    value_total = sum([dic_frecA[x] for x in dic_frecA])
    for item in dic_frecA:
        dic_frecA[item] = porcentaje_neto(value_total, dic_frecA[item])
    return dic_frecA

def frecA(lista):
    frequencyA = Counter(lista)
    return frequencyA

def frecAcum(lista):
    frequencyA = frecA(lista)
    frequencyAcum = calcular_frecAcum(frequencyA)
    return frequencyAcum

def frecR(lista):
    frequencyA = frecA(lista)
    frequencyR = calcular_frecR(frequencyA)
    return frequencyR

def frecA_intervalos(lista, dic_intervalos):
    frequencyA = {}
    for item in dic_intervalos:
        frequencyA[item] = 0
    for i in lista:
        for item in dic_intervalos:
            limite_inicial, limite_final = dic_intervalos[item]
            if limite_inicial <= i <= limite_final:
                frequencyA[item] += 1
                break
    return frequencyA

def frecAcum_intervalos(lista, dic_intervalos):
    frequencyA = frecA_intervalos(lista, dic_intervalos)
    frequencyAcum = calcular_frecAcum(frequencyA)
    return frequencyAcum


def frecR_intervalos(lista, dic_intervalos):
    frequencyA = frecA_intervalos(lista, dic_intervalos)
    frequencyR = calcular_frecR(frequencyA)
    return frequencyR

def porcentaje_neto(total, valor):
    porcentaje = valor / total * 100
    porcentaje = round(porcentaje, 2)
    return porcentaje

def valor_porcentaje(total, valor):
    valorPorcentaje = valor * total / 100
    return valorPorcentaje

def cal_intervalo(lista):
    lista.sort()
    r = rango(lista)
    num_intervalos = math.ceil(math.sqrt(len(lista)))
    tam_intervalos = math.ceil(r / num_intervalos)

    intervalos = ""
    part1_intervalo = []
    part2_intervalo = []

    limite_inicial = min(lista)
    limite_final = limite_inicial + (tam_intervalos - 1)
    part1_intervalo.append((limite_inicial))
    part2_intervalo.append((limite_final))

    while limite_final < max(lista):
        limite_inicial += tam_intervalos
        limite_final += tam_intervalos
        part1_intervalo.append((limite_inicial))
        part2_intervalo.append((limite_final))

    for i in range(len(part1_intervalo)):
        full_intervalo = f"{part1_intervalo[i]} - {part2_intervalo[i]},"
        intervalos += full_intervalo
    return intervalos


def clean_intervalos(lista):
    intervalos = {}
    separacion_intervalos = lista.split(",")
    separacion_intervalos.remove(separacion_intervalos[-1])
    ranges_int = [[int(float(numero)) for numero in intervalo.split("-")]for intervalo in separacion_intervalos]
    for i in range(len(ranges_int)):
        intervalos[separacion_intervalos[i]] = ranges_int[i]
    return intervalos

def presentacion_dicts(dic_normalizado):
    output = ""
    dic_value = True
    for frecuencia, dic_intervalo in dic_normalizado.items():
        if isinstance(dic_intervalo, dict) and dic_value:
            intervalos = ""
            for key, value in dic_intervalo.items():
                intervalos += f"\n{key}: {value}"
            dic_intervalo = intervalos
        else:
            dic_value = False
        output += f"{frecuencia}: {dic_intervalo}\n"
    return output

def normalizar_dicts(dic_frecuencias):
    return {key: value for key, value in sorted(dic_frecuencias.items())}

def eleccion_funciones(oprUser, dic_funciones, *data):
    for key, value in dic_funciones.items():
        if oprUser == key:
            if len(data) == 1 and isinstance(data[0], (list, tuple)):
                return value(data[0])
            else:
                return value(data[0], data[1])

# lista = input("Ingrese los datos separados por comas p.ej. 1, 2, 3, 4, 5: ")
# list_num = [float(x) for x in lista.split(",")]
# intervalos = cal_intervalo(list_num)
# print(intervalos)

opr = ["rango", "varianza", "desviacion estandar", "mediana", "moda", "media", "frecuencia absoluta", "frecuencia acumulada", "frecuencia relativa", "porcentaje", "intervalo"]

opr_dataAislada = {
    "rango": rango,
    "varianza": varianza,
    "desviacion estandar": desviacion_estandar,
    "mediana": mediana,
    "moda": moda,
    "media": media,
    "frecuencia absoluta": frecA,
    "frecuencia acumulada": frecAcum,
    "frecuencia relativa": frecR
}
oprs_intervalos_f = {
    "frecuencia absoluta": frecA_intervalos,
    "frecuencia acumulada": frecAcum_intervalos,
    "frecuencia relativa": frecR_intervalos
}
opr_porcentaje = {
    "neto": porcentaje_neto,
    "valor": valor_porcentaje
}

while True:
    while True:
        oprUser = input(f"Ingrese la operacion a realizar {opr}: ").lower()
        if oprUser not in opr:
            print("Operacion no valida")
        else:
            break

    if oprUser in opr[:-2]:
        while True:
            lista = input("Ingrese los datos separados por comas p.ej. 1, 2, 3, 4, 5: ")
            try:
                list_num = [float(x) for x in lista.split(",")]
                resultado = eleccion_funciones(oprUser, opr_dataAislada, list_num)
                if "frecuencia" in oprUser:
                    resultado = presentacion_dicts(normalizar_dicts(resultado))
                print(f"El resultado de la {oprUser} es: \n{resultado}")
                break
            except ValueError:
                print("Ingrese los datos en el formato correcto")

    elif oprUser == "porcentaje":
        while True:
            try:
                tipo_porcentaje = input("Ingrese el tipo de porcentaje a calcular (neto/valor): ").lower()
                if tipo_porcentaje not in opr_porcentaje.keys():
                    print("Tipo de porcentaje no valido")
                    continue
                else:
                    total = int(input("Ingrese el total: "))
                    valor = int(input("Ingrese el valor o porcentaje: "))
                    resultado = eleccion_funciones(tipo_porcentaje, opr_porcentaje, total, valor)
                resultado = presentacion_dicts(resultado)
                print(f"El resultado de tipo de porcentaje {tipo_porcentaje} es: {resultado}")
                break
            except ValueError:
                print("Ingrese un tipo de dato correcto")

    elif oprUser == "intervalo":
        while True:
            try:
                lista = input("Ingrese los datos separados por comas p.ej. 1, 2, 3, 4, 5: ")
                lista = [float(x) for x in lista.split(",")]
                intervalos = cal_intervalo(lista)
                intervalos = clean_intervalos(intervalos)

                tipo_frecuencia = input("Que frecuencia desea obtener (frecuencia absoluta/frecuencia acumulada/frecuencia relativa/todas): ")
                if tipo_frecuencia == "todas":
                    resultado = {}
                    for key in oprs_intervalos_f.keys():
                        resultado[key] = eleccion_funciones(key, oprs_intervalos_f, lista, intervalos)
                    tipo_frecuencia += " las frecuencias"
                elif "frecuencia" not in tipo_frecuencia:
                    print("Tipo de frecuencia no valido")
                    continue
                else:
                    resultado = eleccion_funciones(tipo_frecuencia, oprs_intervalos_f, lista, intervalos)
                resultado = presentacion_dicts(resultado)
                print(f"El resultado de {tipo_frecuencia} es:\n{resultado}")
                break
            except ValueError:
                print("Ingrese sus datos en el formato correcto")

    continuar = input("¿Desea realizar otra operacion? (si/no): ").lower()
    if continuar in "no":
        break
