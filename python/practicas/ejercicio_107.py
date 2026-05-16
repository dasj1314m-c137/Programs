n = int(input("Ingresa el valor de n: "))
m = int(input("Ingresa el valor de m: "))

if (n < m):
    sumatoria_sigma = 0
    for i in range(n, m + 1):
        sumatoria_sigma += i

    print(f"La sumatoria entre los rangos {n} y {m} es: {sumatoria_sigma}")
else:
    print("n debe ser menor que m")
