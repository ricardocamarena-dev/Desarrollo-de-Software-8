# view_actuators.py - Control de LEDs e Indicadores Sonoros
from machine import Pin, PWM

class ActuatorView:
    def __init__(self, led_armed_pin=16, led_alarm_pin=17, buzzer_pin=15):
        self.led_armed = Pin(led_armed_pin, Pin.OUT)
        self.led_alarm = Pin(led_alarm_pin, Pin.OUT)
        self.buzzer_pin = Pin(buzzer_pin, Pin.OUT)
        self.pwm_buzzer = None

    def update_indicators(self, armed, alarm_active):
        self.led_armed.value(1 if armed else 0)

        if alarm_active:
            self.led_alarm.value(1)
            self.sound_alarm(True)
        else:
            self.led_alarm.value(0)
            self.sound_alarm(False)

    def sound_alarm(self, enable):
        if enable:
            try:
                if not self.pwm_buzzer:
                    self.pwm_buzzer = PWM(self.buzzer_pin)
                    self.pwm_buzzer.freq(1000)
                    self.pwm_buzzer.duty_u16(32768)
            except Exception:
                self.buzzer_pin.value(1)
        else:
            if self.pwm_buzzer:
                self.pwm_buzzer.deinit()
                self.pwm_buzzer = None
            self.buzzer_pin.value(0)
