data = input("Ingrese los datos separados por comas, y le daremos la media: ")
list_nums = [int(x) for x in data.split(",")]
sum_varianza = 0

media = sum(list_nums) / len(list_nums)

for i in list_nums:
    sum_varianza += (i - media)**2

varianza = sum_varianza / len(list_nums)

print(f"La media de los datos {data} es: {round(varianza, 2)}")

