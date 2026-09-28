total_eco = 0
suma_energia_normal = 0.0
contador_normal = 0

while True:
    print("--------------------------------------------------")
    ldr_aux = input("\nIngrese Lectura del LDR (0.0 a 100.0) o -1.0 para salir: ")
    ldr = float(ldr_aux)

    if ldr == -1.0:
        break

    bateria_aux = input("Ingrese nivel de carga de la bateria (%): ")
    bateria = float(bateria_aux)

    if bateria < 20.0:
        brillo = 10.0
        estado = "MODO ECO ACTIVADO"
        accion = f"Bateria baja (20%). Brillo forzado al {brillo:.1f}%."
        total_eco += 1
        
    elif ldr < 40.0:
        brillo = 100.0 - ldr
        estado = "MODO NORMAL"
        accion = f"Brillo de LED calculado: {brillo:.1f}%"
        suma_energia_normal += brillo
        contador_normal += 1
        
    else:
        brillo = 0.0
        estado = "DÍA DETECTADO"
        accion = f"Brillo de LED calculado: {brillo:.1f}% (Apagado)."

    print(f"[{estado}] {accion}")

print("\n SIMULACIÓN FINALIZADA")
print("Lecturas totales en modo ecológico:", total_eco)

if contador_normal > 0:
    promedio_energia = suma_energia_normal / contador_normal
    print(f"Energia utilizada de iluminación promedio: {promedio_energia:.1f}%")
else:
    print("Energia utilizada de iluminación promedio: 0.0%")