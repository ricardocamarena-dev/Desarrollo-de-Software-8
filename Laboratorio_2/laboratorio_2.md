# Universidad Tecnológica de Panamá
**Facultad de Ingeniería de Sistemas Computacionales**  
**Licenciatura en Desarrollo de Software**  

## LABORATORIO #2

---

### Problema 1: Simulador de Invernadero Inteligente

**Contexto:**  
Se requiere automatizar un invernadero agrícola mediante el monitoreo cíclico de temperatura y humedad ambiental. El sistema de software debe adquirir un lote fijo de mediciones, analizar si se superan los niveles seguros del cultivo operativo y consolidar un reporte final.

**Requisitos del Software:**
* Solicitar al operador hasta 5 muestras de telemetría. Cada muestra consta de dos lecturas: la temperatura (°C) y la humedad relativa (de 0 a 100%).
* En caso de que la temperatura supere los **30.0 °C** y la humedad relativa sea superior al **75.0%**, imprimir una alerta inmediata en pantalla: `'¡ALERTA!: Ambiente crítico para hongo'`.
* Llevar un registro acumulado de cuántas alertas críticas ocurrieron. Mostrar el reporte en consola indicando el número total de alertas generadas.
* Si ocurrieron 3 o más alertas, el sistema debe imprimir un aviso adicional: `'ESTADO: Acción correctiva requerida (Activar extractor)'`. De lo contrario, imprimir: `'ESTADO: Sistema Operando Estable'`.

#### Ejemplo de Entrada/Salida en Consola (Problema 1):

```
>>> Ingrese la temperatura de la muestra #1 (°C): 28.5
>>> Ingrese la humedad relativa de la muestra #1 (%): 60.0
>>> Ingrese la temperatura de la muestra #2 (°C): 32.5
>>> Ingrese la humedad relativa de la muestra #2 (%): 80.0
¡ALERTA!: Ambiente crítico para hongo.
>>> Ingrese la temperatura de la muestra #3 (°C): 25.0
>>> Ingrese la humedad relativa de la muestra #3 (%): 55.0
>>> Ingrese la temperatura de la muestra #4 (°C): 31.0
>>> Ingrese la humedad relativa de la muestra #4 (%): 82.0
¡ALERTA!: Ambiente crítico para hongo.
>>> Ingrese la temperatura de la muestra #5 (°C): 33.0
>>> Ingrese la humedad relativa de la muestra #5 (%): 78.0
¡ALERTA!: Ambiente crítico para hongo.
========= REPORTE OPERATIVO FINAL =========
Total de alertas críticas por hongo detectadas: 3
ESTADO: Acción correctiva requerida (Activar extractor).
```

---

### Problema 2: Analizador de Consumo en Smart Grid

**Contexto:**  
En una red eléctrica inteligente (Smart Grid), se despliegan medidores para registrar el consumo eléctrico residencial. Se requiere desarrollar una herramienta local que simule la carga de electrodomésticos en red, calcule el costo del servicio bajo tarifa escalonada y finalice el registro de forma segura.

**Requisitos del Software:**
* Implementar un bucle continuo.
* Solicitar al usuario que ingrese el nombre del electrodoméstico medido, el consumo de potencia del equipo (float, en Watts) y las horas estimadas de uso diario (float). O la palabra clave `'detener'` para finalizar.
* Calcular el consumo total diario en KiloWatts-hora (kWh) mediante la expresión:  
  `kWh = (Watts * horas) / 1000`
* Determinar la tarifa del equipo aplicando un condicional:
  * Para los electrodomésticos con un consumo superior a **2.5 kWh** diarios, el costo por kWh es de **$0.18** (tarifa alta).
  * Si no, el costo por kWh es de **$0.12** (tarifa regular).
* Imprimir el consumo calculated y su costo individual.
* Llevar un registro del consumo total general y del costo económico total para mostrarlos al detenerse el bucle.

#### Ejemplo de Entrada/Salida en Consola (Problema 2):

```
>>> Ingrese el nombre del electrodoméstico (o 'detener'): Refrigeradora
>>> Ingrese consumo de potencia (Watts): 350
>>> Ingrese horas estimadas de uso diario (horas): 24
Consumo calculated: 8.40 kWh | Tarifa: Alta ($0.18/kWh) | Costo: $1.512
>>> Ingrese el nombre del electrodoméstico (o 'detener'): Bombillo LED
>>> Ingrese consumo de potencia (Watts): 12
>>> Ingrese horas estimadas de uso diario (horas): 10
Consumo calculated: 0.12 kWh | Tarifa: Regular ($0.12/kWh) | Costo: $0.014
>>> Ingrese el nombre del electrodoméstico (o 'detener'): detener
========= SMART GRID REPORT =========
Consumo Total Acumulado: 8.52 kWh
Costo Total Acumulado Estimado: $1.53
```

---

### Problema 3: Calibrador Dinámico de Deriva en Sensores de Presión

**Contexto:**  
Los sensores de presión industriales sufren descalibraciones temporales (deriva o *drift*). El software de calibración debe leer de forma secuencial una serie de datos de prueba del sensor, calcular la desviación absoluta respecto al valor patrón de laboratorio y clasificar el lote.

**Requisitos del Software:**
* Establecer un bucle para registrar hasta 10 mediciones secuenciales del sensor.
* Definir el valor de referencia patrón (ejemplo: **1013.25 hPa**, presión estándar).
* Para cada lectura ingresada (en hPa), calcular la desviación absoluta restando la lectura individual del valor de presión estándar.
* En caso de que una lectura individual presente una desviación superior a **5.0 hPa** respecto a la referencia patrón, el programa debe imprimir: `'¡ADVERTENCIA!: Medición fuera de tolerancia'`. De lo contrario, imprimir: `'Estado: Tolerancia aceptable'`.
* Al finalizar el ciclo, calcular la desviación promedio de todo el conjunto de lecturas.
* Clasificar el sensor:
  * Si el promedio de desviación absoluta supera los **3.0 hPa**, imprimir: `'CLASIFICACIÓN: Sensor requiere Recalibración en Laboratorio'`.
  * De lo contrario, imprimir: `'CLASIFICACIÓN: Sensor Aprobado para Operación'`.

#### Ejemplo de Entrada/Salida en Consola (Problema 3):

```
>>> Ingrese la medición de presión #1 (hPa): 1012.0
Desviación absoluta: 1.25 hPa | Estado: Tolerancia aceptable.
>>> Ingrese la medición de presión #2 (hPa): 1005.0
¡ADVERTENCIA!: Medición fuera de tolerancia. Desviación: 8.25 hPa
>>> Ingrese la medición de presión #3 (hPa): 1018.5
¡ADVERTENCIA!: Medición fuera de tolerancia. Desviación: 5.25 hPa
>>> Ingrese la medición de presión #4 (hPa): 1011.0
Desviación absoluta: 2.25 hPa | Estado: Tolerancia aceptable.
========= DIAGNÓSTICO DEL SENSOR =========
Desviación promedio del lote: 4.25 hPa
CLASIFICACIÓN: Sensor requiere Recalibración en Laboratorio.
```

---

### Problema 4: Firewall Lógico de Mensajería para Redes IoT

**Contexto:**  
Un Gateway de seguridad inspecciona de forma secuencial las cabeceras de los paquetes entrantes para evitar intrusiones en la red local de control industrial. El sistema debe simular la inspección, aplicar reglas estrictas de filtrado y evaluar el nivel de amenaza de la sesión.

**Requisitos del Software:**
* Establecer un bucle para inspeccionar un paquete de 5 mensajes consecutivos.
* Para cada paquete, solicitar la entrada de tres datos: el protocolo (`'MQTT'`, `'HTTP'` o `'FTP'`), el tamaño del payload (en bytes) y el puerto de red (ejemplo: 80).
* Definir la regla lógica de bloqueo mediante condicionales:
  * Un paquete será **BLOQUEADO** si:
    * El protocolo es `'HTTP'` y el puerto **no** es el 80.
    * El protocolo es `'FTP'` y el puerto no está en la lista de permitidos (puertos válidos: 20, 21, 22, 990 y del 1024 al 49151, excepto el 3306).
    * El protocolo es `'MQTT'` y el puerto no es 1883, 8883 o 443.
    * El payload supera los **1024 bytes** (independientemente del protocolo).
  * En cualquier otro caso, el paquete se considera **PERMITIDO**.
* Imprimir en pantalla la acción de seguridad correspondiente por cada paquete (`'[ACCIÓN]: BLOQUEADO'` o `'[ACCIÓN]: PERMITIDO'`).
* Llevar un registro de cuántos paquetes fueron bloqueados en total.
* Al finalizar, si el número de paquetes bloqueados supera el 50% del tráfico (3 o más bloqueos), imprimir:  
  `'ESTADO DE LA RED: Alerta Roja, posible intrusión en proceso'`.  
  En caso contrario, imprimir: `'ESTADO DE LA RED: Monitoreo Normal'`.

#### Ejemplo de Entrada/Salida en Consola (Problema 4):

```
>>> [Paquete #1] Ingrese protocolo (MQTT/HTTP/FTP): HTTP
>>> [Paquete #1] Ingrese puerto de red: 8080
>>> [Paquete #1] Ingrese tamaño del payload (bytes): 512
[ACCIÓN]: BLOQUEADO
>>> [Paquete #2] Ingrese protocolo (MQTT/HTTP/FTP): MQTT
>>> [Paquete #2] Ingrese puerto de red: 1883
>>> [Paquete #2] Ingrese tamaño del payload (bytes): 128
[ACCIÓN]: PERMITIDO
>>> [Paquete #3] Ingrese protocolo (MQTT/HTTP/FTP): FTP
>>> [Paquete #3] Ingrese puerto de red: 21
>>> [Paquete #3] Ingrese tamaño del payload (bytes): 64
[ACCIÓN]: BLOQUEADO
>>> [Paquete #4] Ingrese protocolo (MQTT/HTTP/FTP): HTTP
>>> [Paquete #4] Ingrese puerto de red: 80
>>> [Paquete #4] Ingrese tamaño del payload (bytes): 2048
[ACCIÓN]: BLOQUEADO
>>> [Paquete #5] Ingrese protocolo (MQTT/HTTP/FTP): MQTT
>>> [Paquete #5] Ingrese puerto de red: 1883
>>> [Paquete #5] Ingrese tamaño del payload (bytes): 256
[ACCIÓN]: PERMITIDO
========= SEGURIDAD DE RED IOT =========
Total de paquetes bloqueados: 3 de 5
ESTADO DE LA RED: Alerta Roja, posible intrusión en proceso.
```

---

### Problema 5: Controlador Inteligente de Luminarias Públicas (Eco-LED)

**Contexto:**  
Las luminarias urbanas inteligentes regulan su brillo dinámicamente para ahorrar energía basándose en la luz ambiental detectada (sensor LDR) y el porcentaje de batería solar restante en su acumulador. El sistema de software integrado ejecuta un ciclo para evaluar la eficiencia energética.

**Requisitos del Software:**
* Utilizar una estructura de control repetitiva para evaluar las condiciones de funcionamiento indefinidamente.
* En cada iteración, solicitar al usuario que ingrese la Lectura del LDR (de 0.0% a 100.0%) o ingresar `-1.0` para finalizar la simulación.
* Solicitar el nivel de carga de la batería (de 0.0% a 100.0%).
* Determinar la potencia de iluminación aplicando las siguientes reglas de negocio:
  * **a.** Si la batería es inferior a **20.0%**, forzar la luminaria a modo ecológico limitado: `Brillo = 10%` (sin importar el LDR).
  * **b.** Si la batería es mayor o igual a **20.0%** y la lectura LDR es menor al **40.0%** (oscuridad), calcular el brillo como la inversa del LDR: `Brillo = 100% - LDR`.
  * **c.** Si la batería es mayor o igual a **20.0%** y la lectura LDR es mayor o igual al **40.0%** (claridad de día), el brillo debe ser **0%** (Luminaria apagada).
* Imprimir en consola el brillo calculated de forma formateada.
* Llevar una contabilidad de:
  * El número total de lecturas ejecutadas en modo ecológico.
  * El promedio general de energía de iluminación utilizada (excluyendo el modo ecológico y las lecturas de día).

#### Ejemplo de Entrada/Salida en Consola (Problema 5):

```
>>> Ingrese Lectura del LDR (0.0 a 100.0) o -1.0 para salir: 30.0
Ingrese nivel de carga de la batería (%): 85.0
[MODO NORMAL] Brillo de LED calculado: 70.0%
>>> Ingrese Lectura del LDR (0.0 a 100.0) o -1.0 para salir: 45.0
Ingrese nivel de carga de la batería (%): 15.0
[MODO ECO ACTIVADO] Batería baja (<20%). Brillo forzado al 10.0%.
>>> Ingrese Lectura del LDR (0.0 a 100.0) o -1.0 para salir: 55.0
Ingrese nivel de carga de la batería (%): 90.0
[DÍA DETECTADO] Brillo de LED calculado: 0.0% (Apagado).
>>> Ingrese Lectura del LDR (0.0 a 100.0) o -1.0 para salir: -1.0
========= SIMULACIÓN FINALIZADA =========
Lecturas totales en modo ecológico: 1
Energía utilizada de iluminación promedio: 70.0%
```