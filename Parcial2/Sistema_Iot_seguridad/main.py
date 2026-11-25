# main.py - Orquestador principal limpio con validación Wi-Fi/MQTT, cola FIFO en RAM y OLED
import gc
import network
import time
from machine import Pin, time_pulse_us

import config
from model_db import SecurityDataModel
from view_oled import OLEDView
from view_actuators import ActuatorView
from controller_mqtt import MQTTController

# --- Sensores ---
pir_sensor = Pin(config.PIR_PIN, Pin.IN)
trig_pin = Pin(config.TRIG_PIN, Pin.OUT)
echo_pin = Pin(config.ECHO_PIN, Pin.IN)

# --- Botón físico para silenciar la alarma (Emergencia / Fallo de sensor) ---
button = Pin(config.BUTTON_PIN, Pin.IN, Pin.PULL_UP)
_button_pressed = False
_last_press = time.ticks_ms()


def _on_button(pin):
    global _button_pressed, _last_press
    now = time.ticks_ms()
    if time.ticks_diff(now, _last_press) > config.BUTTON_DEBOUNCE_MS:
        _last_press = now
        _button_pressed = True


button.irq(trigger=Pin.IRQ_FALLING, handler=_on_button)

# --- Estado de red y cola en RAM (FIFO) ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wifi_retry_count = 0
_last_wifi_attempt = None
WIFI_RETRY_MS = 5000

MAX_RAM_QUEUE = 25
_pending_queue = []  # Elementos: ("telemetry", payload) o ("event", (event_type, details))
_last_flush_attempt = time.ticks_ms()
FLUSH_RETRY_MS = 3000


def is_wifi_connected():
    if not wlan.active():
        return False
    try:
        ip = wlan.ifconfig()[0]
        if not ip or ip == "0.0.0.0":
            return False
        st = wlan.status()
        # En Pico W (CYW43), 3 equivale a STAT_GOT_IP; valores < 0 indican fallo o desconexión
        if st < 0 or st != 3:
            return False
    except Exception:
        return False
    return bool(wlan.isconnected())


def can_publish_now():
    if not is_wifi_connected():
        if mqtt_ctrl.connected:
            mqtt_ctrl._drop("sin Wi-Fi antes de publicar")
        return False
    return mqtt_ctrl.connected


def ensure_wifi(blocking_initial=False):
    global wifi_retry_count, _last_wifi_attempt
    if is_wifi_connected():
        return True

    now = time.ticks_ms()
    if blocking_initial:
        print("Conectando a Wi-Fi...")
        while not is_wifi_connected():
            wifi_retry_count += 1
            print(f"[Wi-Fi] Intento #{wifi_retry_count} a '{config.WIFI_SSID}'...")
            try:
                wlan.connect(config.WIFI_SSID, config.WIFI_PASS)
            except Exception as e:
                print("[Wi-Fi] Error al iniciar conexión:", e)

            for _ in range(10):
                if is_wifi_connected():
                    print("Wi-Fi conectado. IP:", wlan.ifconfig()[0])
                    return True
                time.sleep(0.5)
        return is_wifi_connected()

    if _last_wifi_attempt is None or time.ticks_diff(now, _last_wifi_attempt) >= WIFI_RETRY_MS:
        _last_wifi_attempt = now
        wifi_retry_count += 1
        print(f"\n[Wi-Fi] Sin red. Reintento #{wifi_retry_count}...")
        try:
            wlan.connect(config.WIFI_SSID, config.WIFI_PASS)
        except Exception as e:
            print("\n[Wi-Fi] Error de conexión:", e)

    return is_wifi_connected()


def queue_payload(kind, data):
    _pending_queue.append((kind, data))
    if len(_pending_queue) > MAX_RAM_QUEUE:
        _pending_queue.pop(0)  # FIFO: descarta el más antiguo solo si se supera el límite
    gc.collect()
    print(f"\n[Cola RAM] Guardado ({kind}). Pendientes: {len(_pending_queue)}")


def send_or_queue_telemetry(payload):
    if can_publish_now():
        try:
            mqtt_ctrl.publish_telemetry(payload)
            return True
        except Exception as e:
            print("\n[MQTT] Falló envío de telemetría:", e)
    else:
        print("\n[Wi-Fi/MQTT] Sin conexión activa para telemetría.")
    queue_payload("telemetry", payload)
    return False


def send_or_queue_event(event_type, details):
    if can_publish_now():
        try:
            mqtt_ctrl.publish_event(event_type, details)
            return True
        except Exception as e:
            print("\n[MQTT] Falló envío de evento:", e)
    else:
        print("\n[Wi-Fi/MQTT] Sin conexión activa para evento.")
    queue_payload("event", (event_type, details))
    return False


def flush_pending_queue():
    global _last_flush_attempt
    if not _pending_queue:
        return
    if not can_publish_now():
        return

    now = time.ticks_ms()
    if time.ticks_diff(now, _last_flush_attempt) < FLUSH_RETRY_MS:
        return
    _last_flush_attempt = now

    while _pending_queue and can_publish_now():
        kind, data = _pending_queue[0]
        try:
            if kind == "telemetry":
                mqtt_ctrl.publish_telemetry(data)
            elif kind == "event":
                ev_type, ev_details = data
                mqtt_ctrl.publish_event(ev_type, ev_details)
            _pending_queue.pop(0)
            print(f"\n[Cola RAM] Reenviado ({kind}). Restantes: {len(_pending_queue)}")
        except Exception as e:
            print(f"\n[Cola RAM] Falló reenvío ({kind}), queda en cola: {e}")
            break


def read_ultrasonic_distance():
    trig_pin.value(0)
    time.sleep_us(2)
    trig_pin.value(1)
    time.sleep_us(10)
    trig_pin.value(0)
    try:
        duration = time_pulse_us(echo_pin, 1, 30000)
        distance = (duration * 0.0343) / 2
        return distance if distance > 0 else 400.0
    except Exception:
        return 400.0


# --- Inicialización ---
ensure_wifi(blocking_initial=True)

model = SecurityDataModel()
oled = OLEDView(sda_pin=config.I2C_SDA_PIN, scl_pin=config.I2C_SCL_PIN)
actuators = ActuatorView(
    led_armed_pin=config.LED_ARMED_PIN,
    led_alarm_pin=config.LED_ALARM_PIN,
    buzzer_pin=config.BUZZER_PIN,
)


def process_command(command, origin):
    cmd = command.strip().upper()
    if cmd == "HISTORY":
        send_or_queue_event("REQUEST_HISTORY", {"origin": origin})
    else:
        model.handle_command(cmd, origin)


mqtt_ctrl = MQTTController(process_command)


def render_oled(dist_cm, pir_state):
    oled.update_status(
        model.system_armed,
        model.alarm_active,
        dist_cm,
        pir_state,
    )
    if oled.display:
        net_ok = is_wifi_connected() and mqtt_ctrl.connected
        net_label = "NET:OK" if net_ok else f"NO-NET#{wifi_retry_count}"
        q_label = f"Q:{len(_pending_queue)}" if _pending_queue else ""
        oled.display.fill_rect(68, 0, 60, 10, 0)
        oled.display.text(net_label[:7], 68, 0)
        if q_label:
            oled.display.fill_rect(88, 54, 40, 10, 0)
            oled.display.text(q_label, 88, 54)
        oled.display.show()


def refresh_views():
    actuators.update_indicators(model.system_armed, model.alarm_active)
    render_oled(model.last_distance_cm, model.last_pir_state)


# --- Control de eventos y envío inmediato ---
last_telemetry = time.ticks_ms()


def on_model_event(event, data):
    global last_telemetry
    refresh_views()

    if event == "INTRUSION_DETECTED":
        send_or_queue_event("INTRUSION_DETECTED", data)
        send_or_queue_telemetry(model.build_telemetry_payload())
        print(f"\n[MQTT] ¡Alerta! Telemetría procesada por intrusión (Zona: {data.get('zone')}).")
        last_telemetry = time.ticks_ms()

    elif event == "STATE_CHANGED":
        pass

    elif event == "COMMAND_EXECUTED":
        send_or_queue_event("COMMAND_ACK", data)


model.subscribe(on_model_event)
if is_wifi_connected():
    mqtt_ctrl.connect()
refresh_views()

print("Sistema de Seguridad IoT inicializado.")

# --- Bucle principal ---
while True:
    try:
        wifi_ok = is_wifi_connected()
        mqtt_ok = False
        if not wifi_ok:
            if mqtt_ctrl.connected:
                mqtt_ctrl._drop("Wi-Fi desconectado")
            ensure_wifi(blocking_initial=False)
        else:
            mqtt_ctrl.ensure_connected()
            mqtt_ctrl.check_messages()
            mqtt_ok = mqtt_ctrl.verify_connection(ping_interval_ms=10000)

        if wifi_ok and mqtt_ok:
            flush_pending_queue()

        if _button_pressed:
            _button_pressed = False
            if model.alarm_active:
                print("\nBotón: alarma silenciada (Emergencia / Fallo de sensor)")
                process_command("CLEAR_ALARM", "BUTTON")

        pir_state = bool(pir_sensor.value())
        dist_cm = read_ultrasonic_distance()

        model.process_sensor_readings(pir_state, dist_cm)
        render_oled(dist_cm, pir_state)

        current_time = time.ticks_ms()
        elapsed_ms = time.ticks_diff(current_time, last_telemetry)
        interval_ms = config.SUPABASE_INTERVAL_S * 1000
        remaining_sec = max(0, (interval_ms - elapsed_ms) // 1000)

        is_online = wifi_ok and mqtt_ok
        net_state_txt = (
            "ONLINE"
            if is_online
            else f"OFFLINE (Wi-Fi:{int(wifi_ok)} MQTT:{int(mqtt_ok)} Retries:{wifi_retry_count} Cola:{len(_pending_queue)})"
        )
        print(
            f"[Pico W] {net_state_txt} | Zona: {getattr(model, 'current_zone', 'SEGURA')} | Próx. MQTT: {remaining_sec}s   ",
            end="\r",
        )

        if elapsed_ms >= interval_ms:
            payload = model.build_telemetry_payload()
            if send_or_queue_telemetry(payload):
                print(f"\n[MQTT] Telemetría periódica enviada (Distancia: {dist_cm:.1f}cm).")
            else:
                print(f"\n[Cola RAM] Sin conexión: telemetría guardada en cola (Distancia: {dist_cm:.1f}cm).")
            last_telemetry = time.ticks_ms()

        time.sleep(0.5)

    except Exception as e:
        print("\nError en el ciclo principal:", e)
        time.sleep(1)