# Universidad Tecnológica de Panamá

**FISC | Desarrollo de Software**

## LABORATORIO #1 (Fundamentos de Python)

---

### Problema 1

**Contexto:**

Un microcontrolador lee el voltaje analógico enviado por un sensor de temperatura lineal. El voltaje reportado oscila entre 0.0 V (que representa 0.0 °C) y 3.3 V (que representa 100.0 °C). Como desarrollador de software, debe programar la fórmula matemática de calibración para que el usuario ingrese el voltaje actual y el sistema le devuelva la temperatura calculada en grados Celsius (°C).

**Requisitos del Programa:**

* Solicitar al usuario que ingrese el voltaje medido mediante la consola (utilice `input()`).
* Realizar la conversión explícita del valor de entrada (*casting*) de cadena de texto a decimal (`float`).
* Aplicar la fórmula de conversión lineal: `Temperatura = (Voltaje * 100) / 3.3`
* Mostrar la salida de información: el voltaje ingresado y la temperatura equivalente con dos decimales (ej. `Temperatura calculada: 25.45 °C`).

#### Ejemplo de Entrada/Salida en Consola (Problema 1):

```
>>> Ingrese el voltaje medido (0.0 a 3.3 V): 1.5
Voltaje de Entrada: 1.5 V
Temperatura Calculada: 45.45 °C
--- Ejecución finalizada con éxito
```

---

### Problema 2

**Contexto:**

En la sala de servidores de la FISC, se requiere un software que clasifique la temperatura ambiental e indique a través de mensajes el estado de climatización. Usted debe escribir una estructura condicional que evalúe el valor numérico ingresado por el operador y determine la acción de alerta pertinente.

**Requisitos del Programa:**

* Solicitar al usuario que ingrese la temperatura actual de la sala en grados Celsius (°C).
* Convertir la entrada del usuario a tipo decimal.
* Evaluar de forma óptima utilizando estructura condicional:
  * Cuando la temperatura sea de 20.0 °C o menos: Mostrar `'Estado: Óptimo'` y `'Acción: Mantener ventilación normal'`.
  * Si sobrepasa los 20.0 °C pero no es mayor a 25.0 °C: Mostrar `'Estado: Advertencia'` y `'Acción: Activar ventilación auxiliar'`.
  * Cuando supere los 25.0 °C: Mostrar `'Estado: Alarma Crítica (Peligro de Sobrecalentamiento)'` y `'Acción: Apagar servidores no esenciales e iniciar refrigeración máxima'`.

#### Ejemplo de Entrada/Salida en Consola (Problema 2):

```
>>> Ingrese la temperatura de la sala (°C): 26.5
Estado: Alarma Crítica (Peligro de Sobrecalentamiento)
Acción: Apagar servidores no esenciales e iniciar refrigeración máxima

>>> Ingrese la temperatura de la sala (°C): 18.2
Estado: Óptimo
Acción: Mantener ventilación normal
```

---

### Problema 3

**Contexto:**

Un nodo sensor en un campo agrícola ubicado en Coclé recopila lecturas de humedad de suelo secuenciales. Para evitar reportar falsas lecturas debido al ruido físico, los programadores promedian un bloque de lecturas antes de enviar los datos finales. Debe desarrollar un programa que automatice esta tarea solicitando una cantidad fija de lecturas utilizando un bucle iterativo controlado.

**Requisitos del Programa:**

* Solicitar al usuario el número total de lecturas que desea simular (ej. `¿Cuántas lecturas va a registrar?: `).
* Registrar la suma total de las lecturas.
* Utilizar un bucle iterativo para solicitar al usuario que ingrese cada lectura de humedad secuencialmente (las lecturas de humedad son valores decimales entre 0% y 100%).
* Calcular el promedio de humedad y mostrar el resultado por pantalla formateado a un decimal.

#### Ejemplo de Entrada/Salida en Consola (Problema 3):

```
>>> ¿Cuántas lecturas va a registrar?: 3
Ingrese la lectura de humedad #1 (%): 45.5
Ingrese la lectura de humedad #2 (%): 50.2
Ingrese la lectura de humedad #3 (%): 48.3
Total de lecturas procesadas: 3
Humedad Promedio del Suelo: 48.0 %
```

---

### Problema 4

**Contexto:**

Un sensor ultrasónico mide continuamente el nivel de agua de una represa de seguridad. El sistema debe ejecutarse indefinidamente hasta que un operador ingrese un comando de apagado seguro. Adicionalmente, el software debe ser inmune a fallos de entrada, en caso de que el usuario ingrese accidentalmente un valor no numérico.

**Requisitos del Programa:**

* Solicitar al operador que ingrese el nivel actual del agua en metros, o la palabra clave `'salir'` para detener el sistema.
* Si el usuario ingresó el texto exacto `'salir'`, mostrar un mensaje de apagado seguro (`Apagando el sistema de monitoreo de represa...`).
* Implementar un bloque de manejo de errores (`try-except`) para evitar que el script colapse ante entradas inválidas.
* En caso de que el nivel sea mayor a 4.5 metros, imprimir una alerta de peligro: `'¡ALERTA!: Nivel de agua crítico. Peligro de desbordamiento'`. De lo contrario, imprimir `'Nivel estable'`.

#### Ejemplo de Entrada/Salida en Consola (Problema 4):

```
>>> Ingrese el nivel de agua (m) o 'salir': 3.2
Nivel estable.
>>> Ingrese el nivel de agua (m) o 'salir': 4.8
¡ALERTA!: Nivel de agua crítico. Peligro de desbordamiento.
>>> Ingrese el nivel de agua (m) o 'salir': agua123
Error: Entrada no válida. Por favor ingrese un número decimal o escriba 'salir'.
>>> Ingrese el nivel de agua (m) o 'salir': salir
Apagando el sistema de monitoreo de represa...
Proceso finalizado de forma segura
```

---

### Entregable

Se debe subir a Teams a la carpeta de Laboratorios, subcarpeta `"laboratorio1"`, con el nombre de la carpeta indicando la numeración del grupo; así: `"Grupo1"`, `"Grupo2"`, etc.