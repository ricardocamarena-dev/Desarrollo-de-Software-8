import json
import time
import requests
import paho.mqtt.client as mqtt
from supabase import create_client, Client

# --- Configuración de Supabase ---
SUPABASE_URL = "https://aepcqadeylbqvmraknoa.supabase.co"
SUPABASE_KEY = "sb_publishable_hVt-D5Uu-5GewU8KTp19Jg_c9_rR7ZR"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- Configuración de ThingSpeak ---
THINGSPEAK_WRITE_API_KEY = "4HJJI0K4X6Z2R93R" 
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# --- Configuración MQTT ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "utp/parcial2/seguridad/#" 

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("[MQTT] ¡Conectado exitosamente al broker MQTT!")
        client.subscribe(MQTT_TOPIC)
        print(f"[MQTT] Suscrito al tópico: {MQTT_TOPIC}")
    else:
        print(f"[MQTT] Error de conexión. Código de retorno: {rc}")

def on_disconnect(client, userdata, rc, properties=None):
    print(f"[MQTT] Desconectado del broker (Código: {rc}). Intentando reconectar...")

def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        
        timestamp_str = time.strftime('%H:%M:%S')
        print(f"\n[MQTT Recibido] Tópico: {topic} [{timestamp_str}]")
        
        if "telemetria" in topic:
            distance = data.get("distance_cm")
            if distance is None:
                distance = data.get("distance", 0.0)
                
            if distance is not None:
                distance = round(float(distance), 2)
            else:
                distance = 0.0
            
            zone = data.get("zone", "SEGURA")
            
            motion = data.get("pir_motion")
            if motion is None:
                motion = data.get("pir")
            if motion is None:
                motion = data.get("pir_state", False)
                
            motion_val = 1.0 if (motion is True or motion == 1 or motion == 1.0) else 0.0
            
            # Guardar en Supabase
            rows = [
                {"sensor_name": "HC-SR04_Distancia", "value": distance, "unit": "cm"},
                {"sensor_name": "PIR_Movimiento", "value": motion_val, "unit": "binary"}
            ]
            supabase.table("sensor_readings").insert(rows).execute()
            print(f"[Supabase Guardado] Zona: {zone} | Distancia: {distance} cm | Movimiento PIR: {motion_val}")

            # Enviar a ThingSpeak
            try:
                ts_payload = {
                    "api_key": THINGSPEAK_WRITE_API_KEY,
                    "field1": 1,
                    "field2": 1 if motion_val == 1.0 else 0,
                    "field3": distance,
                    "field4": int(motion_val)
                }
                response = requests.post(THINGSPEAK_URL, data=ts_payload, timeout=5)
                print(f"[ThingSpeak] Telemetría enviada. HTTP Status: {response.status_code}")
            except Exception as ts_err:
                print(f"[ThingSpeak] Error al enviar telemetría: {ts_err}")

        elif "eventos" in topic:
            event_type_raw = data.get("tipo") or data.get("event") or data.get("evento")
            
            if event_type_raw == "COMMAND_ACK":
                cmd_data = data if "command" in data else data.get("details", {})
                row = {
                    "command_name": cmd_data.get("command"),
                    "origin": cmd_data.get("origin"),
                    "status": cmd_data.get("status", "OK")
                }
                supabase.table("executed_commands").insert(row).execute()
                print(f"[Supabase] Comando registrado en BD: {row['command_name']} desde {row['origin']}")
            else:
                zone = data.get("zone") or data.get("zona") or "PELIGRO"
                
                distance = data.get("distance_cm")
                if distance is None:
                    distance = data.get("distance")
                if distance is None and isinstance(data.get("details"), dict):
                    distance = data.get("details").get("distance_cm") or data.get("details").get("distance")
                
                if distance is not None:
                    distance = round(float(distance), 2)
                else:
                    distance = 0.0
                
                pir = data.get("pir")
                if pir is None:
                    pir = data.get("pir_motion", False)
                if pir is None and isinstance(data.get("details"), dict):
                    pir = data.get("details").get("pir", False)
                
                tipo_evento = f"ZONA_{zone.upper()}"
                desc = f"Zona: {zone.upper()} | PIR: {pir} | Distancia: {distance}cm"
                    
                row = {
                    "event_type": tipo_evento,
                    "description": desc,
                    "severity_level": "ALTA" if zone.upper() == "PELIGRO" else "MEDIA"
                }
                supabase.table("security_events").insert(row).execute()
                print(f"[Supabase Guardado] Evento registrado -> Tipo: {tipo_evento} | {desc}")

    except Exception as e:
        print("[Error Procesando Mensaje]:", e)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print("Iniciando puente MQTT -> Supabase & ThingSpeak...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDeteniendo puente MQTT...")
    client.loop_stop()
    client.disconnect()