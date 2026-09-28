t = 5
alertas = 0

for i in range(1, t + 1):
    
    print("---------------------------------------------------------------")
    temp_input = input(f"Ingrese la temperatura de la muestra #{i} (°C): ")
    temp = float(temp_input)
    
    hum_input = input(f"Ingrese la humedad relativa de la muestra #{i} (%): ")
    humedad = float(hum_input)

    if temp > 30.0 and humedad > 75.0:
        print("¡!ALERTA!!: Ambiente crítico para hongo.")
        alertas += 1


print("REPORTE OPERATIVO FINAL")
print("Total de alertas críticas por hongo detectadas:", alertas)

if alertas >= 3:
    print("ESTADO: Acción correctiva requerida (Activar extractor).")
else:
    print("ESTADO: Sistema Operando Estable")