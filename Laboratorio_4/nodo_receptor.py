import json
import os
from datetime import datetime

# Nombre del archivo que vamos a leer
nombre_archivo = "lecturas_sensores.json"

if not os.path.exists(nombre_archivo):
    print(f"\nError: No encontré el archivo '{nombre_archivo}'")
    print("Primero debes ejecutar nodo_emisor.py")
    exit()

print(f"Archivo encontrado: {nombre_archivo}\n")

# CARGAR EL JSON
try:
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)
    print("Archivo JSON cargado correctamente\n")
except:
    print("Error: El archivo JSON está dañado")
    exit()

# VER CUÁLES SENSORES TENEMOS
sensores_disponibles = list(datos.keys())

print("SENSORES DISPONIBLES:")
for i, sensor in enumerate(sensores_disponibles, 1):
    cantidad = len(datos[sensor]["lecturas"])
    unidad = datos[sensor]["unidad"]
    print(f"  {i}. {sensor.upper()} ({cantidad} lecturas) [{unidad}]")

# PEDIR AL USUARIO QUE ELIJA UN SENSOR
print()
while True:
    try:
        opcion = int(input("Elige el número del sensor: "))
        if 1 <= opcion <= len(sensores_disponibles):
            sensor_elegido = sensores_disponibles[opcion - 1]
            break
        else:
            print("Número no válido")
    except:
        print("Debes escribir un número")

# OBTENER LOS DATOS DEL SENSOR ELEGIDO
unidad = datos[sensor_elegido]["unidad"]
lecturas = datos[sensor_elegido]["lecturas"]

lecturas_normales = []
lecturas_criticas = []

for lectura in lecturas:
    if lectura["critica"]:
        lecturas_criticas.append(lectura)
    else:
        lecturas_normales.append(lectura)

# MOSTRAR EN PANTALLA
print(f"Total de lecturas: {len(lecturas)}")
print(f"Normales: {len(lecturas_normales)}")
print(f"Críticas: {len(lecturas_criticas)}\n")

# Mostrar normales
if lecturas_normales:
    print("LECTURAS NORMALES:")
    for lectura in lecturas_normales:
        print(f"  - Ciclo {lectura['ciclo']}: {lectura['valor']} {unidad}")

print()

# Mostrar críticas
if lecturas_criticas:
    print("LECTURAS CRÍTICAS:")
    for lectura in lecturas_criticas:
        print(f"  - Ciclo {lectura['ciclo']}: {lectura['valor']} {unidad}")

# CREAR INFORME EN ARCHIVO TXT
nombre_informe = f"informe_{sensor_elegido}.txt"
informe = ""

# Crear el contenido del informe
informe += f"INFORME DE LECTURAS DE SENSOR\n"
informe += f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
informe += f"Sensor: {sensor_elegido.upper()}\n"
informe += f"Unidad: {unidad}\n"
informe += f"Total de lecturas: {len(lecturas)}\n\n"


informe += f"Lecturas NORMALES: {len(lecturas_normales)}\n"
informe += f"Lecturas CRÍTICAS: {len(lecturas_criticas)}\n\n"

# Agregar lecturas normales
if lecturas_normales:
    informe += "-" * 80 + "\n"
    informe += "LECTURAS NORMALES/CORRECTAS\n"
    for i, lectura in enumerate(lecturas_normales, 1):
        informe += f"{i}. Ciclo: {lectura['ciclo']}\n"
        informe += f"   Valor: {lectura['valor']} {unidad}\n"
        informe += f"   Estado: DENTRO DE RANGO SEGURO\n\n"

# Agregar lecturas críticas
if lecturas_criticas:
    informe += "-" * 80 + "\n"
    informe += "LECTURAS CRÍTICAS/FUERA DE RANGO\n"
    for i, lectura in enumerate(lecturas_criticas, 1):
        informe += f"{i}. Ciclo: {lectura['ciclo']}\n"
        informe += f"   Valor: {lectura['valor']} {unidad}\n"
        informe += f"   Estado: FUERA DE RANGO SEGURO\n\n"

# Guardar en archivo
with open(nombre_informe, 'w', encoding='utf-8') as archivo:
    archivo.write(informe)

print(f"\nInforme guardado en: {nombre_informe}")
