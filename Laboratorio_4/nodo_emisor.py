import json
import random

sensores = [
    {
        "nombre": "temperatura",
        "unidad": "°C",
        "rango_generacion": (10.0, 45.0),
        "limite_min_seguro": 15.0,
        "limite_max_seguro": 35.0,
    },
    {
        "nombre": "humedad",
        "unidad": "%",
        "rango_generacion": (10.0, 100.0),
        "limite_min_seguro": 20.0,
        "limite_max_seguro": 80.0,
    },
    {
        "nombre": "presion",
        "unidad": "hPa",
        "rango_generacion": (950.0, 1050.0),
        "limite_min_seguro": 980.0,
        "limite_max_seguro": 1030.0,
    },
]

# Diccionario principal: cada dispositivo guarda su lista de lecturas
dispositivos = {
    sensor["nombre"]: {
        "unidad": sensor["unidad"],
        "lecturas": []
    }
    for sensor in sensores
}


def es_lectura_critica(valor, sensor):
    """Retorna True si el valor está fuera del rango seguro del sensor."""
    return valor < sensor["limite_min_seguro"] or valor > sensor["limite_max_seguro"]


def pedir_ciclos():
    while True:
        entrada = input("Ingrese el número de ciclos a ejecutar: ")
        try:
            ciclos = int(entrada)
            if ciclos <= 0:
                print("Error: el número de ciclos debe ser mayor a 0.")
                continue
            return ciclos
        except ValueError:
            print("Error: ingrese un número entero válido.")


# Bucle principal de generación de lecturas
num_ciclos = pedir_ciclos()

for ciclo_actual in range(1, num_ciclos + 1):
    print(f"\n=== Ciclo {ciclo_actual} de {num_ciclos} ===")

    for sensor in sensores:
        minimo, maximo = sensor["rango_generacion"]
        valor = round(random.uniform(minimo, maximo), 2)
        critica = es_lectura_critica(valor, sensor)

        lectura = {
            "ciclo": ciclo_actual,
            "valor": valor,
            "critica": critica,
        }
        dispositivos[sensor["nombre"]]["lecturas"].append(lectura)

        ciclos_pendientes = num_ciclos - ciclo_actual
        estado = "CRÍTICA" if critica else "normal"
        print(f"  Sensor '{sensor['nombre']}': {valor} {sensor['unidad']} "
              f"[{estado}] - Ciclos pendientes: {ciclos_pendientes}")

# Guardado en archivo JSON

nombre_archivo = "lecturas_sensores.json"

with open(nombre_archivo, "w", encoding="utf-8") as archivo:
    json.dump(dispositivos, archivo, indent=4, ensure_ascii=False)

print("\n---------------------------")
print(f"Proceso finalizado. Datos guardados en '{nombre_archivo}'.")
