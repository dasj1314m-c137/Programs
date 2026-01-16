data = input("Ingrese los datos separados por comas, y le daremos la media: ")
list_nums = [int(x) for x in data.split(",")]

media = sum(list_nums) / len(list_nums)

print(f"La media de los datos {data} es: {round(media, 2)}")