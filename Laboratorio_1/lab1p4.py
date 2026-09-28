while True:
    entrada = input("ingrese el nivel del agua en (m) o 'salir':")
    if entrada == "salir":
        print("apagando el sistema de monitoreo de represa...")
        break
    try:
        nivel = float(entrada)
        if nivel > 4.5:
            print("ALERTA!: EL NIVEL DEL AGUA ES CRITICO A DESBORDAMIENTO")
        else:
            print("Nivel de agua estable.")
    except ValueError:
            print("Error: valor invalido, inserte un numero decimal o 'salir'")
print("--- Proceso finalizado de forma segura ---")
        