import json
import os
import threading
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
MQTT_BASE_TOPIC = "utp/parcial2/seguridad/utp2026_r1"
MQTT_TOPIC = f"{MQTT_BASE_TOPIC}/#"
MQTT_ACK_TOPIC = f"{MQTT_BASE_TOPIC}/ack"

# --- Cola temporal en JSON ---
QUEUE_FILE = "offline_queue.json"
MAX_QUEUE_ITEMS = 500
FLUSH_INTERVAL_S = 10
queue_lock = threading.Lock()
reconnect_attempts = 0


def load_queue():
    if not os.path.exists(QUEUE_FILE):
        return []
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception as e:
        print(f"[Cola JSON] Error leyendo {QUEUE_FILE}, iniciando vacía: {e}")
        return []


def save_queue(queue):
    tmp_file = QUEUE_FILE + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)
    os.replace(tmp_file, QUEUE_FILE)


def enqueue_item(target, payload):
    with queue_lock:
        queue = load_queue()
        entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "target": target,
            "payload": payload,
        }
        queue.append(entry)
        if len(queue) > MAX_QUEUE_ITEMS:
            queue = queue[-MAX_QUEUE_ITEMS:]
        save_queue(queue)
        print(f"[Cola JSON] Guardado pendiente ({target}). Total en cola: {len(queue)}")


def send_item(item):
    target = item.get("target")
    payload = item.get("payload")

    if target == "supabase_readings":
        supabase.table("sensor_readings").insert(payload).execute()
    elif target == "supabase_events":
        supabase.table("security_events").insert(payload).execute()
    elif target == "supabase_commands":
        supabase.table("executed_commands").insert(payload).execute()
    elif target == "thingspeak":
        response = requests.post(THINGSPEAK_URL, data=payload, timeout=5)
        response.raise_for_status()


def flush_queue():
    with queue_lock:
        queue = load_queue()
        if not queue:
            return

        remaining = []
        for idx, item in enumerate(queue):
            try:
                send_item(item)
                print(f"[Cola JSON] Reenviado ({item.get('target')}) con fecha {item.get('timestamp')}")
            except Exception as e:
                print(f"[Cola JSON] Aún sin conexión para ({item.get('target')}): {e}")
                remaining = queue[idx:]
                break

        save_queue(remaining)


def dispatch_or_queue(target, payload):
    try:
        send_item({"target": target, "payload": payload})
        return True
    except Exception as e:
        print(f"[Envío directo falló -> {target}]: {e}")
        enqueue_item(target, payload)
        return False


def publish_ack(client, msg_id, status="OK"):
    if not msg_id:
        return
    try:
        client.publish(MQTT_ACK_TOPIC, json.dumps({"msg_id": msg_id, "status": status}))
    except Exception as e:
        print(f"[ACK] Error enviando ACK para {msg_id}: {e}")


def on_connect(client, userdata, connect_flags, reason_code, properties=None):
    global reconnect_attempts
    if reason_code == 0 or str(reason_code) == "Success":
        reconnect_attempts = 0
        print("[MQTT] ¡Conectado exitosamente al broker MQTT!")
        client.subscribe(MQTT_TOPIC)
        print(f"[MQTT] Suscrito al tópico: {MQTT_TOPIC}")
        flush_queue()
    else:
        reconnect_attempts += 1
        print(f"[MQTT] Error de conexión (Intento #{reconnect_attempts}). Código: {reason_code}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties=None):
    global reconnect_attempts
    reconnect_attempts += 1
    print(f"[MQTT] Desconectado del broker (Intento reconexión #{reconnect_attempts}, Código: {reason_code}). Reintentando...")


def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        if topic == MQTT_ACK_TOPIC:
            return

        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        timestamp_str = time.strftime("%H:%M:%S")
        print(f"\n[MQTT Recibido] Tópico: {topic} [{timestamp_str}]")

        all_ok = True

        if "telemetria" in topic:
            distance = data.get("distance_cm")
            if distance is None:
                distance = data.get("distance", 0.0)

            distance = round(float(distance), 2) if distance is not None else 0.0
            zone = data.get("zone", "SEGURA")

            motion = data.get("pir_motion")
            if motion is None:
                motion = data.get("pir")
            if motion is None:
                motion = data.get("pir_state", False)

            motion_val = 1.0 if (motion is True or motion == 1 or motion == 1.0) else 0.0
            alarm_val = 1 if (motion_val == 1.0 or zone == "PELIGRO") else 0

            rows = [
                {"sensor_name": "HC-SR04_Distancia", "value": distance, "unit": "cm"},
                {"sensor_name": "PIR_Movimiento", "value": motion_val, "unit": "binary"},
            ]
            ok_sb = dispatch_or_queue("supabase_readings", rows)
            if ok_sb:
                print(f"[Supabase Guardado] Zona: {zone} | Distancia: {distance} cm | Movimiento PIR: {motion_val}")

            ts_payload = {
                "api_key": THINGSPEAK_WRITE_API_KEY,
                "field1": 1,
                "field2": alarm_val,
                "field3": distance,
                "field4": int(motion_val),
            }
            ok_ts = dispatch_or_queue("thingspeak", ts_payload)
            if ok_ts:
                print("[ThingSpeak] Telemetría enviada correctamente.")

            all_ok = ok_sb and ok_ts

        elif "eventos" in topic:
            event_type_raw = data.get("tipo") or data.get("event") or data.get("evento")

            if event_type_raw == "COMMAND_ACK":
                cmd_data = data if "command" in data else data.get("details", {})
                row = {
                    "command_name": cmd_data.get("command"),
                    "origin": cmd_data.get("origin"),
                    "status": cmd_data.get("status", "OK"),
                }
                all_ok = dispatch_or_queue("supabase_commands", row)
                if all_ok:
                    print(f"[Supabase] Comando registrado en BD: {row['command_name']} desde {row['origin']}")
            else:
                zone = data.get("zone") or data.get("zona") or "PELIGRO"

                distance = data.get("distance_cm")
                if distance is None:
                    distance = data.get("distance")
                if distance is None and isinstance(data.get("details"), dict):
                    distance = data.get("details").get("distance_cm") or data.get("details").get("distance")

                distance = round(float(distance), 2) if distance is not None else 0.0

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
                    "severity_level": "ALTA" if zone.upper() == "PELIGRO" else "MEDIA",
                }
                all_ok = dispatch_or_queue("supabase_events", row)
                if all_ok:
                    print(f"[Supabase Guardado] Evento registrado -> Tipo: {tipo_evento} | {desc}")

        msg_id = data.get("msg_id")
        if msg_id:
            publish_ack(client, msg_id, status="OK" if all_ok else "QUEUED")

    except Exception as e:
        print("[Error Procesando Mensaje]:", e)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

print("Iniciando puente MQTT -> Supabase & ThingSpeak...")
while True:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        break
    except Exception as e:
        reconnect_attempts += 1
        print(f"[MQTT] Sin conexión inicial (Intento #{reconnect_attempts}): {e}")
        flush_queue()
        time.sleep(5)

client.loop_start()

try:
    while True:
        flush_queue()
        time.sleep(FLUSH_INTERVAL_S)
except KeyboardInterrupt:
    print("\nDeteniendo puente MQTT...")
    client.loop_stop()
    client.disconnect()