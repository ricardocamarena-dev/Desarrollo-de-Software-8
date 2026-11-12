# controller_mqtt.py - Controlador de comunicación MQTT (HiveMQ)
import json
import time
from umqttsimple import MQTTClient
import config


class MQTTController:
    """Gestiona la conexión MQTT. No conoce vistas ni modelo: los comandos
    recibidos se delegan a `command_handler(command, origin)`."""

    def __init__(self, command_handler):
        self.command_handler = command_handler
        self.client = None
        self._last_attempt = None
        self._last_ping = time.ticks_ms()

    @property
    def connected(self):
        return self.client is not None

    def connect(self):
        self._last_attempt = time.ticks_ms()
        try:
            print("Conectando al broker MQTT...")
            client = MQTTClient(config.MQTT_CLIENT_ID, config.MQTT_BROKER,
                                port=config.MQTT_PORT,
                                keepalive=config.MQTT_KEEPALIVE)
            client.set_callback(self._on_message_received)
            client.connect()
            client.subscribe(config.MQTT_TOPIC_COMMANDS)
            self.client = client
            self._last_ping = time.ticks_ms()
            print("MQTT conectado. Comandos en:", config.MQTT_TOPIC_COMMANDS)
            return True
        except Exception as e:
            print("MQTT no disponible (modo local):", e)
            self.client = None
            return False

    def ensure_connected(self):
        """Reintenta la conexión cada MQTT_RETRY_SECONDS si está caída."""
        if self.client is not None:
            return
        if (self._last_attempt is None or
                time.ticks_diff(time.ticks_ms(), self._last_attempt)
                >= config.MQTT_RETRY_SECONDS * 1000):
            self.connect()

    def _drop(self, reason):
        print("MQTT desconectado:", reason)
        try:
            self.client.disconnect()
        except Exception:
            pass
        self.client = None

    def check_messages(self):
        if not self.client:
            return
        try:
            self.client.check_msg()
            if time.ticks_diff(time.ticks_ms(), self._last_ping) >= config.MQTT_PING_SECONDS * 1000:
                self.client.ping()
                self._last_ping = time.ticks_ms()
        except Exception as e:
            self._drop(e)

    def _publish(self, topic, data):
        if not self.client:
            return
        try:
            self.client.publish(topic, json.dumps(data))
        except Exception as e:
            self._drop(e)

    def publish_telemetry(self, data):
        self._publish(config.MQTT_TOPIC_TELEMETRY, data)

    def publish_event(self, event_type, details):
        self._publish(config.MQTT_TOPIC_EVENTS, {"event": event_type, "details": details})

    def _on_message_received(self, topic, msg):
        command = msg.decode("utf-8")
        print("Comando MQTT recibido:", command)
        self.command_handler(command, "MQTT")
