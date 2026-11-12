# main.py - Orquestador principal (orientado a eventos) para Raspberry Pi Pico W
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

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Conectando a Wi-Fi...")
        wlan.connect(config.WIFI_SSID, config.WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Wi-Fi conectado. IP:", wlan.ifconfig()[0])

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
connect_wifi()

model = SecurityDataModel()
oled = OLEDView(sda_pin=config.I2C_SDA_PIN, scl_pin=config.I2C_SCL_PIN)
actuators = ActuatorView(
    led_armed_pin=config.LED_ARMED_PIN,
    led_alarm_pin=config.LED_ALARM_PIN,
    buzzer_pin=config.BUZZER_PIN
)

def process_command(command, origin):
    cmd = command.strip().upper()
    if cmd == "HISTORY":
        mqtt_ctrl.publish_event("REQUEST_HISTORY", {"origin": origin})
    else:
        model.handle_command(cmd, origin)

mqtt_ctrl = MQTTController(process_command)

def refresh_views():
    actuators.update_indicators(model.system_armed, model.alarm_active)
    oled.update_status(model.system_armed, model.alarm_active,
                         model.last_distance_cm, model.last_pir_state)

# --- Control de eventos y envío inmediato ---
last_telemetry = time.ticks_ms()

def on_model_event(event, data):
    global last_telemetry
    refresh_views()
    
    if event == "INTRUSION_DETECTED":
        mqtt_ctrl.publish_event("INTRUSION_DETECTED", data)
        mqtt_ctrl.publish_telemetry(model.build_telemetry_payload())
        print(f"\n[MQTT] ¡Alerta! Telemetría enviada de inmediato por intrusión (Zona: {data.get('zone')}).")
        last_telemetry = time.ticks_ms()
        
    elif event == "STATE_CHANGED":
        pass
        
    elif event == "COMMAND_EXECUTED":
        mqtt_ctrl.publish_event("COMMAND_ACK", data)

model.subscribe(on_model_event)
mqtt_ctrl.connect()
refresh_views()

print("Sistema de Seguridad IoT inicializado.")

# --- Bucle principal ---
while True:
    try:
        mqtt_ctrl.ensure_connected()
        mqtt_ctrl.check_messages()

        if _button_pressed:
            _button_pressed = False
            if model.alarm_active:
                print("\nBotón: alarma silenciada (Emergencia / Fallo de sensor)")
                process_command("CLEAR_ALARM", "BUTTON")

        pir_state = bool(pir_sensor.value())
        dist_cm = read_ultrasonic_distance()

        model.process_sensor_readings(pir_state, dist_cm)
        oled.update_status(model.system_armed, model.alarm_active, dist_cm, pir_state)

        current_time = time.ticks_ms()
        elapsed_ms = time.ticks_diff(current_time, last_telemetry)
        interval_ms = config.SUPABASE_INTERVAL_S * 1000
        remaining_sec = max(0, (interval_ms - elapsed_ms) // 1000)

        print(f"[Pico W] Zona: {getattr(model, 'current_zone', 'SEGURA')} | Próx. MQTT Periódico: {remaining_sec}s   ", end="\r")

        if elapsed_ms >= interval_ms:
            mqtt_ctrl.publish_telemetry(model.build_telemetry_payload())
            print(f"\n[MQTT] Telemetría periódica enviada al puente (Distancia: {dist_cm:.1f}cm).")
            last_telemetry = time.ticks_ms()

        time.sleep(0.5)

    except Exception as e:
        print("\nError en el ciclo principal:", e)
        time.sleep(1)