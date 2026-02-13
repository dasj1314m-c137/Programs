import matplotlib.pyplot as plt

num_students = [23, 20, 7, 3]
labels = ["Suspensos", "Aprobado", "Notable", "Sobresaliente"]

plt.pie(num_students, labels=labels, autopct="%.2f%%")
plt.show()
