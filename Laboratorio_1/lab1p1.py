print ("ingrese el voltaje medido (0.0 a 3.3 v): 1,5")
voltaje = input ("ingrese el voltaje medido: ")
v = float (voltaje)
temperatura =(v * 100)/3.3
    
    
print ("voltaje calculado: ", v, "V")

print ("temperatura calculada:", round(temperatura,2),"°C")
