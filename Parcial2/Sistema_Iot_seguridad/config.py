# config.py - Configuración Global para Raspberry Pi Pico W

ID_SUFFIX = "utp2026_r1"

# --- Wi-Fi (Simulación Wokwi) ---
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASS = ""

# --- Broker MQTT HiveMQ público ---
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "pico_w_sec_" + ID_SUFFIX
MQTT_KEEPALIVE = 60
MQTT_RETRY_SECONDS = 30   
MQTT_PING_SECONDS = 30
_BASE = "utp/parcial2/seguridad/" + ID_SUFFIX
MQTT_TOPIC_TELEMETRY = _BASE + "/telemetria"
MQTT_TOPIC_COMMANDS = _BASE + "/comandos"
MQTT_TOPIC_EVENTS = _BASE + "/eventos"

# --- ThingSpeak (Dashboard + comandos vía TalkBack) ---
THINGSPEAK_URL = "http://api.thingspeak.com/update"
THINGSPEAK_WRITE_API_KEY = "4HJJI0K4X6Z2R93R"
THINGSPEAK_INTERVAL_S = 20      

# TalkBack: crea uno en ThingSpeak (Apps > TalkBack) y pega aquí sus datos.
TALKBACK_ID = "TU_TALKBACK_ID"
TALKBACK_API_KEY = "TU_TALKBACK_API_KEY"
TALKBACK_INTERVAL_S = 25

# --- Supabase (PostgreSQL vía REST) ---
SUPABASE_URL = "https://aepcqadeylbqvmraknoa.supabase.co/rest/v1"
SUPABASE_KEY = "sb_publishable_hVt-D5Uu-5GewU8KTp19Jg_c9_rR7ZR"
SUPABASE_INTERVAL_S = 60

# --- Pines GPIO (Raspberry Pi Pico W) ---
PIR_PIN = 28
TRIG_PIN = 3
ECHO_PIN = 2
BUZZER_PIN = 15
LED_ARMED_PIN = 16
LED_ALARM_PIN = 17

BUTTON_PIN = 14       # GP14 - Botón físico para silenciar la alarma (a GND, pull-up interno)
BUTTON_DEBOUNCE_MS = 250

# --- I2C0 ---
I2C_SDA_PIN = 0
I2C_SCL_PIN = 1

# --- Umbrales ---
DISTANCIAS_UMBRAL_CM = 20.0
ALARM_SILENCE_S = 10   # tras silenciar, los sensores se ignoran este tiempo