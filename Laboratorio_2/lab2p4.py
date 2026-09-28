bloqueados = 0

for i in range(1, 6):
    protocolo = input(f"[Paquete #{i}] Ingrese protocolo (MQTT/HTTP/FTP): ")
    puerto = int(input(f"[Paquete #{i}] Ingrese puerto de red: "))
    payload = int(input(f"[Paquete #{i}] Ingrese tamaño del payload (bytes): "))

    bloqueado = False
    
    if protocolo not in ("MQTT", "HTTP", "FTP"):
        bloqueado = True
        
    if payload > 1024:
        bloqueado = True

    if protocolo == "HTTP":
        if puerto != 80:
            bloqueado = True

    elif protocolo == "FTP":
        puertos_validos_ftp = (puerto in (20, 21, 22, 990)) or (1024 <= puerto <= 49151 and puerto != 3306)
        if not puertos_validos_ftp:
            bloqueado = True

    elif protocolo == "MQTT":
        if puerto not in (1883, 8883, 443):
            bloqueado = True

    if bloqueado:
        print("[ACCIÓN]: BLOQUEADO")
        bloqueados = bloqueados + 1
    else:
        print("[ACCIÓN]: PERMITIDO")

    print()  

print("=============  ESTADO DE LA RED  =============")
print(f"Paquetes bloqueados: {bloqueados} de 5")

if bloqueados >= 3:
    print("ESTADO DE LA RED: Alerta Roja, posible intrusión en proceso.")
else:
    print("ESTADO DE LA RED: Monitoreo Normal.")