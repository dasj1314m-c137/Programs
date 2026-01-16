precio = int(input("Ingrese el precio y calcularemos el precion con IVA: "))
suma_IVA = (16 * precio) / 100
precio_IVA = precio + suma_IVA

print(f"El precio {precio} con IVA es: {precio_IVA}")