# controller_cloud.py - Supabase (BD remota) + ThingSpeak (dashboard y comandos)
import urequests
import json
import gc
import time
import config

class CloudController:
    def __init__(self):
        # rstrip evita la doble barra (.../v1//tabla)
        self.supabase_url = config.SUPABASE_URL.rstrip("/")
        self.supabase_key = config.SUPABASE_KEY
        self.thingspeak_url = config.THINGSPEAK_URL
        self.thingspeak_key = config.THINGSPEAK_WRITE_API_KEY
        self._queue = []
        self._cooldown_until = time.ticks_ms()
        self._MAX_QUEUE = 20
        self._COOLDOWN_MS = 20000

    # ================= HTTP con reintentos =================
    def _request(self, method, url, headers, data=None, retries=2, delay=3):
        """HTTP/HTTPS con reintentos. Devuelve (status, texto) o (None, None)."""
        headers = dict(headers)
        headers["Connection"] = "close"
        for intento in range(retries):
            gc.collect()  
            time.sleep(0.5)
            try:
                if method == "POST":
                    res = urequests.post(url, headers=headers, data=data)
                else:
                    res = urequests.get(url, headers=headers)
                status, body = res.status_code, res.text
                res.close()
                return status, body
            except Exception as e:
                print("[HTTP] intento {}/{} falló: {}".format(intento + 1, retries, e))
                if intento < retries - 1:
                    time.sleep(delay * (intento + 1))
        return None, None

    # ================= SUPABASE =================
    def _headers(self):
        return {
            "apikey": self.supabase_key,
            "Authorization": "Bearer " + self.supabase_key,
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }

    def _post(self, table, data):
        """Encola el INSERT y trata de vaciar la cola. True si se envió."""
        self._queue.append((table, json.dumps(data)))
        if len(self._queue) > self._MAX_QUEUE:
            self._queue.pop(0)  # descarta lo más viejo para no agotar la RAM
        sent = self._flush()
        if not sent:
            print("[Supabase] En cola, pendientes:", len(self._queue))
        return sent

    def _flush(self):
        """Envía la cola en orden. Se detiene al primer fallo de red."""
        if not self._queue:
            return True
        if time.ticks_diff(self._cooldown_until, time.ticks_ms()) > 0:
            return False  
        while self._queue:
            table, body = self._queue[0]
            status, _ = self._request(
                "POST", "{}/{}".format(self.supabase_url, table),
                self._headers(), body)
            if status is None or status >= 500:
                self._cooldown_until = time.ticks_add(time.ticks_ms(), self._COOLDOWN_MS)
                return False
            if status >= 300:
                print("[Supabase]", table, "rechazado HTTP", status, "- descartado")
            self._queue.pop(0)
        return True

    def insert_sensor_readings(self, readings):
        """readings: lista de (nombre, valor, unidad). Un solo POST para todas."""
        rows = [{"sensor_name": n, "value": v, "unit": u} for (n, v, u) in readings]
        if self._post("sensor_readings", rows):
            print("[Supabase] Lecturas guardadas:", len(rows))

    def insert_security_event(self, event_type, description, severity):
        if self._post("security_events", {
                "event_type": event_type,
                "description": description,
                "severity_level": severity}):
            print("[Supabase] Evento registrado:", event_type)

    def insert_command(self, name, origin, status):
        if self._post("executed_commands", {
                "command_name": name, "origin": origin, "status": status}):
            print("[Supabase] Comando registrado:", name, origin, status)

    def get_history(self, table, limit=10):
        """Consulta histórica: últimas `limit` filas, más recientes primero."""
        url = "{}/{}?select=*&order=timestamp.desc&limit={}".format(
            self.supabase_url, table, limit)
        headers = {
            "apikey": self.supabase_key,
            "Authorization": "Bearer " + self.supabase_key,
            "Accept": "application/json"
        }
        status, body = self._request("GET", url, headers)
        if status is None or status >= 300:
            return []
        try:
            return json.loads(body)
        except Exception as e:
            print("[Supabase] Respuesta no válida:", e)
            return []

    # ================= THINGSPEAK =================
    def send_to_thingspeak(self, armed, alarm, distance, motion):
        payload = "api_key={}&field1={}&field2={}&field3={:.1f}&field4={}".format(
            self.thingspeak_key,
            1 if armed else 0,
            1 if alarm else 0,
            distance,
            1 if motion else 0
        )
        try:
            res = urequests.post(
                self.thingspeak_url, data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"})
            print("[ThingSpeak] Telemetría enviada. HTTP:", res.status_code)
            res.close()
        except Exception as e:
            print("[ThingSpeak] Error al enviar telemetría:", e)

    def fetch_talkback_command(self):
        """Pide el siguiente comando pendiente de TalkBack (lo ejecuta y consume).
        Retorna el texto del comando o None si no hay ninguno."""
        if "TU_" in config.TALKBACK_ID or "TU_" in config.TALKBACK_API_KEY:
            return None
        url = "http://api.thingspeak.com/talkbacks/{}/commands/execute".format(
            config.TALKBACK_ID)
        try:
            res = urequests.post(
                url,
                data="api_key={}".format(config.TALKBACK_API_KEY),
                headers={"Content-Type": "application/x-www-form-urlencoded"})
            body = res.text
            res.close()
            if not body or not body.strip():
                return None
            return json.loads(body).get("command_string")
        except Exception as e:
            print("[TalkBack] Sin comando / error:", e)
            return None