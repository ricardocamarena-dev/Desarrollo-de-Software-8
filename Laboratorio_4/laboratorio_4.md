# Laboratorio #4: Arquitectura Emisor / Receptor (JSON)

Esta sesión práctica se desarrollará colaborativamente entre **parejas de grupos (Grupo A y Grupo B)**.

---

## Rol 1: Grupo A — Nodo Emisor

El **Grupo A** debe desarrollar el script que cumpla con las siguientes funciones:

* **Rol:** Asumirá el rol de **Nodo Emisor**, generando lecturas de cada dispositivo y estructurando los datos en un archivo `.json`.
* **Estructura de Datos:** Mediante el uso de listas y diccionarios, se representarán los sensores. Deben incluirse al menos **3 tipos de sensores distintos** (ejemplo: temperatura, humedad, presión, movimiento, etc.).
* **Control de Ciclos:** Debe recibir el número de ciclos a ejecutar e imprimir en consola el estado de los ciclos pendientes de cada dispositivo.
* **Persistencia:** Al finalizar el proceso, el programa debe guardar la lista completa de dispositivos en el archivo `.json`.
* **Alertas:** Dentro del archivo `.json`, se debe incluir un dato para identificar si la lectura es **crítica** o **fuera de rango seguro** (los umbrales y valores quedan a discreción del grupo).

---

## Rol 2: Grupo B — Gateway Receptor

El **Grupo B** debe desarrollar el script que cumpla con las siguientes funciones:

* **Rol:** Asumirá el rol de **Gateway Receptor**, leyendo el archivo generado por el Grupo A.
* **Validación:** Aplicar las validaciones necesarias al leer y procesar el archivo `.json` (manejo de errores y archivo no encontrado).
* **Búsqueda y Filtrado:** El script debe permitir buscar un sensor específico dentro del archivo `.json` y extraer sus lecturas.
* **Análisis de Datos:** Con las lecturas obtenidas, identificar todas las lecturas clasificadas como críticas o fuera de rango.
* **Generación de Reporte:** Exportar los resultados a un archivo `.txt`. El informe debe mostrar de manera clara cuáles lecturas resultaron `"normales/correctas"` y cuáles `"críticas/fuera de rango"`.

---

## Coordinación y Entregable

1. **Intercambio de Datos:** El **Grupo A** colocará el archivo `.json` en Teams (en la ubicación indicada por el profesor) para que posteriormente el **Grupo B** lo utilice en su script.
2. **Comunicación:** Debe existir coordinación directa entre ambos grupos para establecer y estandarizar la estructura del JSON, nombres de claves, tipos de datos y formatos antes de la ejecución.