consumo_total = 0
costo_total = 0

while True:
    electrodomestico = input("ingrese el nombre del electrodomestico (o 'detener'):")
    
    if electrodomestico.lower() == "detener":
        break
    
    watts = float(input(">>> Ingrese consumo de potencia (watts): "))
    horas = float(input(">>> Ingrese horas estimadas de uso diario (horas): "))
    
    # Calculo de consumo en kwh
    consumo = (watts * horas) / 1000
    
    # Tarifa
    if consumo > 2.5:
        tarifa = 0.18
        tipo_tarifa = "Alta"
    else:
        tarifa = 0.12
        tipo_tarifa = "Regular"
        
    costo = consumo * tarifa
    
    consumo_total += consumo
    costo_total += costo
    
    print(f"Consumo calculado: {consumo:.2f} kWh | "
          f"Tarifa: {tipo_tarifa} (${tarifa:.2f}/kWh) | "
          f"Costo: ${costo:.3f}")
    
print("================ SMART GRID REPORT ================")
print(f"Consumo Total Acumulado: {consumo_total:.2f} kWh")
print(f"Costo Total Acumulado Estimado: ${costo_total:.2f}")
    