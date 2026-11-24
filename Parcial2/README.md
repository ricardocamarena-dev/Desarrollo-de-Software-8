# Sistema de Monitoreo y Seguridad IoT con Raspberry Pi Pico W

Este proyecto implementa una arquitectura de Internet de las Cosas (IoT) de extremo a extremo para el monitoreo ambiental y control de seguridad. El sistema captura datos mediante sensores locales, los transmite utilizando protocolos ligeros y los procesa para su almacenamiento persistente y visualización en tiempo real en la nube.

---
## Integrantes y roles

| Integrante | Rol/Aporte |
|---|---|
| Alexander toribio | Hardware y simulación Wokwi |
| Ricardo Camarena | Desarrollo Python y MQTT |
| Miguel Caballero | Base de datos y servicios de nube |
| Luis Sanchez | Documentación y evidencias |

## Arquitectura del Sistema

El proyecto está dividido en tres capas principales que garantizan un flujo de datos desacoplado, escalable y eficiente:

1. **Capa de Percepción (Edge / Hardware Simulado):** 
   - **Raspberry Pi Pico W (Wokwi):** Captura lecturas periódicas de sensores, gestiona estados de alerta y recibe comandos de control. Empaqueta la información en formato **JSON** y la publica a través del protocolo **MQTT**.
2. **Capa de Transporte e Intermediación (Gateway / Bridge):** 
   - **Broker MQTT (HiveMQ):** Gestiona la mensajería entre el microcontrolador y el servidor local mediante tópicos específicos.
   - **Bridge en Python (PC Local):** Actúa como puerta de enlace (*Gateway*). Intercepta los mensajes MQTT, normaliza los datos (aplicando redondeo binario y decimal) y gestiona el envío seguro hacia los servicios en la nube.
3. **Capa de Persistencia y Visualización (Cloud):**
   - **Supabase (Base de Datos Relacional):** Almacena el historial completo dividido en tres tablas especializadas:
     - `sensor_readings`: Telemetría periódica con marca de tiempo (*timestamp*).
     - `security_events`: Registro de alertas críticas categorizadas por zona.
     - `executed_commands`: Auditoría y confirmación de los comandos enviados al dispositivo.
   - **ThingSpeak:** Dashboard en tiempo real que separa visualmente las métricas continuas del estado operativo y las alarmas.

---

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de contar con lo siguiente:

- **Python 3.8+** instalado en tu computadora.
- **Librerías de Python requeridas** para el Bridge (ej. `paho-mqtt`, `supabase`, `requests`, `python-dotenv`).
- Acceso a una cuenta de **Wokwi** (o extensión en VS Code) con el código del microcontrolador cargado.
- Credenciales activas de **HiveMQ**, **Supabase** y **ThingSpeak** configuradas en tus variables de entorno (`.env`).

---

## Guía de Ejecución (Paso a Paso)

Para garantizar que no se pierda ningún paquete de datos inicial, es fundamental iniciar primero el servicio receptor (Bridge) y posteriormente el emisor (Wokwi).

### Paso 1: Configurar el entorno del Bridge
Abre una terminal en la carpeta raíz de tu proyecto en tu PC e instala las dependencias necesarias (si aún no lo has hecho):

```bash
pip install paho-mqtt supabase requests python-dotenv
```

Asegúrate de que tu archivo `.env` contenga las claves de acceso correctas para el broker MQTT, la URL/Key de Supabase y el API Key de ThingSpeak.

### Paso 2: Ejecutar el Bridge (Puerta de Enlace)
En la misma terminal, inicia el script de Python encargado de escuchar los tópicos MQTT y subir la información a la nube:

```bash
python bridge.py
```
*(Nota: Reemplaza `bridge.py` con el nombre exacto de tu archivo principal de Python).*

Verifica en la consola que aparezca el mensaje de conexión exitosa al broker de HiveMQ y que el sistema está en espera de mensajes.

### Paso 3: Iniciar la simulación en Wokwi
1. Abre tu proyecto en **Wokwi**.
2. Verifica que las credenciales de red Wi-Fi (`Wokwi-GUEST`) y los datos del broker MQTT coincidan con los del Bridge.
3. Haz clic en el botón **Start Simulation** (Play).

### Paso 4: Verificación del Flujo de Datos
1. **En Wokwi:** Observa el monitor serial para confirmar que la Pico W se conectó al Wi-Fi y está publicando los payloads en formato JSON.
2. **En la terminal del Bridge:** Verás reflejados los mensajes entrantes, su normalización y la confirmación de inserción exitosa en la base de datos.
3. **En la Nube:** 
   - Ingresa a tu panel de **Supabase** para comprobar los nuevos registros en `sensor_readings`, `security_events` o `executed_commands`.
   - Abre tu canal de **ThingSpeak** para visualizar las gráficas actualizándose en tiempo real.