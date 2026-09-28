print ("ingrese la temperatura de la sala (°C): 26.5")
temp = input ("ingrese el voltaje medido: ")
t = float (temp)

if t <= 20.0:
    estado = "optimo"
    accion ="Mantener ventilacion normal"
elif t <= 25.0:
    estado = "advertencia"
    accion ="Activar ventilacion auxiliar"
else:
    estado = "Alarma critica(Peligro de Sobrecalentamiento)"
    accion ="Apagar servidores no esenciales e iniciar refrigeracion"
    
print("Estado:", estado)
print("Accion:", accion)