import math

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
    return sum(lista) / len(lista)


def moda(lista):
    frequency = {}
    for item in lista:
        if item not in frequency:
            frequency[item] = 1
        else:
            frequency[item] += 1
    max_freq = max(frequency.values())
    modes = [key for key, value in frequency.items() if value == max_freq]
    if len(modes) == len(frequency):
        return None
    for mode in modes:
        return mode
    

def frecA(lista):
    resultado = ""
    frequencyA = {}
    for item in lista:
        if item not in frequencyA:
            frequencyA[item] = 1
        else:
            frequencyA[item] += 1
    for item in frequencyA:
        resultado += f"\n{item} - {frequencyA[item]}"
    return resultado


def frecAcum(lista):
    resultado = ""
    frecuenciaAcum = 0
    frequencyA = {}
    for item in lista:
        if item not in frequencyA:
            frequencyA[item] = 1
        else:
            frequencyA[item] += 1
    for item in frequencyA:
        frecuenciaAcum += frequencyA[item]
        frequencyA[item] = frecuenciaAcum
    for item in frequencyA:
        resultado += f"\n{item} -> {frequencyA[item]}"
    return resultado


def frecR(lista):
    resultado = ""
    frequencyA = {}
    for item in lista:
        if item not in frequencyA:
            frequencyA[item] = 1
        else:
            frequencyA[item] += 1
    value_total = [frequencyA[x] for x in frequencyA]
    for item in frequencyA:
        frequencyA[item] = porcentaje_neto(value_total, frequencyA[item])
    for item in frequencyA:
        resultado += f"\n{item} -> {frequencyA[item]}"
    return resultado


def frecA_intervalos(lista, dic_intervalos):
    resultado = ""
    frequencyA = {}
    for item in dic_intervalos:
        frequencyA[item] = 0
    for i in lista:
        for item in dic_intervalos:
            limite_inicial, limite_final = dic_intervalos[item]
            if limite_inicial <= i <= limite_final:
                frequencyA[item] += 1
                break     
    for item in frequencyA:
        resultado += f"\nLa frecuencia absoluta de {item} es: {frequencyA[item]}"
    return resultado


def frecAcum_intervalos(lista, dic_intervalos):
    resultado = ""
    frecuenciaAcum = 0
    frequencyA = {}
    for item in dic_intervalos:
        frequencyA[item] = 0
    for i in lista:
        for item in dic_intervalos:
            limite_inicial, limite_final = dic_intervalos[item]
            if limite_inicial <= i <= limite_final:
                frequencyA[item] += 1
                break     
    for item in frequencyA:
        frecuenciaAcum += frequencyA[item]
        frequencyA[item] = frecuenciaAcum
    for item in frequencyA:
        resultado += f"\nLa frecuencia acumulada de {item} es: {frequencyA[item]}"
    return resultado


def frecR_intervalos(lista, dic_intervalos):
    resultado = ""
    frequencyA = {}
    for item in dic_intervalos:
        frequencyA[item] = 0
    for i in lista:
        for item in dic_intervalos:
            limite_inicial, limite_final = dic_intervalos[item]
            if limite_inicial <= i <= limite_final:
                frequencyA[item] += 1
                break     
    value_total = [frequencyA[x] for x in frequencyA]
    for item in frequencyA:
        frequencyA[item] = porcentaje_neto(value_total, frequencyA[item])
    for item in frequencyA:
        resultado += f"\nLa frecuencia relativa de {item} es: {frequencyA[item]}%"
    return resultado


def porcentaje_neto(lista, valor):
    total = sum(lista)
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
    separacion_intervalos.remove("")
    ranges_int = [[int(numero) for numero in intervalo.split("-")]for intervalo in separacion_intervalos]

    for i in range(len(ranges_int)):
        intervalos[separacion_intervalos[i]] = ranges_int[i]

    return intervalos


while True:
    opr = ["rango","varianza", "desviacion estandar","mediana", "moda", "media", "porcentaje", "frecuencia absoluta", "frecuencia acumulada", "frecuencia relativa", "intervalo"]
    while True:
        oprUser = input(f"Ingrese la operacion a realizar {opr}: ").lower()
        if oprUser not in opr:
            print("Operacion no valida")
        else:
            break

    if oprUser in ["rango", "varianza", "desviacion estandar", "mediana", "moda", "media", "porcentaje", "frecuencia absoluta", "frecuencia acumulada", "frecuencia relativa"]:
        while True:
            lista = input("Ingrese los datos separados por comas p.ej. 1, 2, 3, 4, 5: ")
            try:
                list_num = [float(x) for x in lista.split(",")]
                if oprUser == "mediana":
                    resultado = mediana(list_num)
                elif oprUser == "moda":
                    resultado = moda(list_num)
                elif oprUser == "media":
                    resultado = media(list_num)
                elif oprUser == "frecuencia absoluta":
                    resultado = frecA(list_num)
                elif oprUser == "frecuencia acumulada":
                    resultado = frecAcum(list_num)
                elif oprUser == "frecuencia relativa":
                    resultado = frecR(list_num)
                elif oprUser == "rango":
                    resultado = rango(list_num)
                elif oprUser == "varianza":
                    resultado = varianza(list_num)
                elif oprUser == "desviacion estandar":
                    resultado = desviacion_estandar(list_num)
                print(f"El resultado de la {oprUser} es: {resultado}")
                break
            except ValueError:
                print("Ingrese sus datos en el formato correcto")
            finally: 
                print()

    elif oprUser == "porcentaje":
        while True:
            try:
                tipo_porcentaje = input("Ingrese el tipo de porcentaje a calcular (neto/valor): ").lower()
                if tipo_porcentaje == "neto":
                    list = input("Ingrese los datos separados por comas p.ej. 1, 2, 3, 4, 5: ")
                    list_num = [float(x) for x in list.split(",")]
                    valor = float(input("Ingrese el valor para calcular el porcentaje neto: "))
                    resultado = porcentaje_neto(list_num, valor)
                    print(f"El porcentaje neto del valor {valor} es: {resultado}%")
                elif tipo_porcentaje == "valor":
                    total = float(input("Ingrese el valor total: "))
                    valor = float(input("Ingrese el porcentaje para calcular el valor: "))
                    resultado = valor_porcentaje(total, valor)
                    print(f"El valor correspondiente al {valor}% de {total} es: {resultado}")
                else:
                    print("Tipo de porcentaje no valido")
                    continue
                break
            except ValueError:
                print("Ingrese un tipo de dato correcto")
            finally:
                print()

    elif oprUser == "intervalo":        
        while True:
            try:
                lista = input("Ingrese los datos separados por comas p.ej. 1, 2, 3, 4, 5: ")
                lista = [int(x) for x in lista.split(",")]
                intervalos = cal_intervalo(lista)
                intervalos = clean_intervalos(intervalos)

                perform_frecuencia = input("Que frecuencia desea obtener (frecuencia absoluta/frecuencia acumulada/frecuencia relativa/todas): ")
                if perform_frecuencia == "frecuencia absoluta":
                    resultado = frecA_intervalos(lista, intervalos)
                elif perform_frecuencia == "frecuencia acumulada":
                    resultado = frecAcum_intervalos(lista, intervalos)
                elif perform_frecuencia == "frecuencia relativa":
                    resultado = frecR_intervalos(lista, intervalos)
                elif perform_frecuencia == "todas":
                    perform_frecuencia += " las frecuencias"
                    frecuenciaA = frecA_intervalos(lista, intervalos)
                    frecuenciaAcum = frecAcum_intervalos(lista, intervalos)
                    frecuenciaR = frecR_intervalos(lista, intervalos)
                    resultado = f"{frecuenciaA}\n{frecuenciaAcum}\n{frecuenciaR}\n"
                else:
                    print("Tipo de frecuencia no valido")
                    continue
                print(f"El resultado de {perform_frecuencia} es:\n{resultado}")
                break
            except ValueError:
                print("Ingrese sus datos en el formato correcto")
            finally:
                print()

    continuar = input("¿Desea realizar otra operacion? (si/no): ").lower()
    if continuar in "no":
        break