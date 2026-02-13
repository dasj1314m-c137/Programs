import matplotlib.pyplot as plt

num_students = []
labels = ["Sus", "Apr", "Not", "Sob"]

num_students.append(float(input("Numero de suspensos: ")))
num_students.append(float(input("Numero de aprobados: ")))
num_students.append(float(input("Numero de notables: ")))
num_students.append(float(input("Numero de sobresalientes: ")))

plt.title("Calificaciones de los estudiantes")
plt.xlabel("Calificaciones")
plt.ylabel("Numero de estudiantes")

plt.bar(labels, num_students)
plt.show()
