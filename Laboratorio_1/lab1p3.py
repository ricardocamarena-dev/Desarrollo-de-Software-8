total_lecturas = int(input("¿Cuántas lecturas va a registrar?: "))


suma_total = 0.0


for i in range(total_lecturas):
    lectura = float(input("Ingrese la lectura de humedad #1 (%) : "))
    suma_total = suma_total + lectura


promedio = suma_total / total_lecturas


print("Total de las lecturas procesadas:", round(suma_total, 1))
print("Humedad promedio del suelo:", round(promedio, 1))