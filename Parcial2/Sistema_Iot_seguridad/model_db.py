# model_db.py - Modelo MVC: estado del sistema, reglas de seguridad y eventos
import time
import config


class SecurityDataModel:
    """Mantiene el estado y notifica cambios a los suscriptores (patrón observer).

    Eventos emitidos (callback(event, data)):
      - INTRUSION_DETECTED : la alarma pasa de normal a activa
      - STATE_CHANGED      : cambia armado/alarma (por comando o cambio de zona)
      - COMMAND_EXECUTED   : se procesó un comando (data: command, origin, status)
    """

    def __init__(self):
        self.system_armed = True
        self.alarm_active = False
        self.last_pir_state = False
        self.last_distance_cm = 0.0
        self.current_zone = "SEGURA"  
        self._listeners = []
        self._silenced_until = time.ticks_ms() 

    # --- Observer ---
    def subscribe(self, callback):
        self._listeners.append(callback)

    def _emit(self, event, data=None):
        for cb in self._listeners:
            try:
                cb(event, data)
            except Exception as e:
                print("Error en listener de", event, ":", e)

    # --- Reglas de seguridad actualizadas ---
    def process_sensor_readings(self, pir_state, dist_cm):
        self.last_distance_cm = dist_cm
        self.last_pir_state = pir_state

        if dist_cm > 100:
            self.current_zone = "SEGURA"
        elif 50 <= dist_cm <= 100:
            self.current_zone = "INTERMEDIA"
        else:
            self.current_zone = "PELIGRO"

        is_silenced = time.ticks_diff(time.ticks_ms(), self._silenced_until) < 0

        if self.system_armed and not is_silenced:
            if self.current_zone == "PELIGRO":
                if not self.alarm_active:
                    self.alarm_active = True
                    self._emit("INTRUSION_DETECTED", {
                        "distance": dist_cm,
                        "zone": self.current_zone,
                        "pir": pir_state
                    })
            else:

                if self.alarm_active:
                    self.alarm_active = False
                    self._emit("STATE_CHANGED", None)
        elif is_silenced and self.alarm_active:
            self.alarm_active = False
            self._emit("STATE_CHANGED", None)

    # --- Comandos (misma lógica para MQTT y ThingSpeak) ---
    def handle_command(self, command, origin):
        cmd = command.strip().upper()
        status = "OK"

        if cmd == "ARM":
            self.set_system_armed(True)
        elif cmd == "DISARM":
            self.set_system_armed(False)
        elif cmd == "CLEAR_ALARM":
            self.clear_alarm()
        else:
            status = "INVALID"

        self._emit("COMMAND_EXECUTED", {
            "command": cmd, "origin": origin, "status": status
        })
        return status == "OK"

    def clear_alarm(self):
        """Silencia la alarma de emergencia (útil si el sensor falla y se queda sonando)."""
        self.alarm_active = False
        self._silenced_until = time.ticks_add(
            time.ticks_ms(), config.ALARM_SILENCE_S * 1000)
        self._emit("STATE_CHANGED", None)

    def set_system_armed(self, status):
        self.system_armed = status
        if not status:
            self.alarm_active = False  # Desarmar apaga la alarma
        self._emit("STATE_CHANGED", None)

    def build_telemetry_payload(self):
        return {
            "timestamp": time.time(),
            "armed": self.system_armed,
            "alarm": self.alarm_active,
            "pir_motion": True if self.alarm_active else self.last_pir_state,
            "distance_cm": round(self.last_distance_cm, 2),
            "zone": getattr(self, "current_zone", "SEGURA")  # Envía la zona actual en la telemetría
        }