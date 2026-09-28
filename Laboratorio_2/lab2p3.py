presion_base = 1013.25

suma_desviacion = 0

for i in range(1, 11):
    lectura = float(input(f"ingresar la medición de presión #{i} (hPa): "))
    
    desviacion = abs(lectura - presion_base)
    suma_desviaciones = suma_desviacion + desviacion

    if desviacion > 5.0:
        print(f"¡ADVERTENCIA!: Medición fuera de tolerancia. Desviación: {desviacion:.2f} hPa")
    else:
        print(f"Desviación absoluta: {desviacion:.2f} hPa | Estado: Tolerancia aceptable.")

promedio_desviacion = suma_desviaciones / 10

print("=============  DIAGNÓSTICO DEL SENSOR  =============")
print(f"Desviación promedio del lote: {promedio_desviacion:.2f} hPa")

if promedio_desviacion > 3.0:
    print("CLASIFICACIÓN: Sensor requiere Recalibración en Laboratorio.")
else:
    print("CLASIFICACIÓN: Sensor Aprobado para Operación.")