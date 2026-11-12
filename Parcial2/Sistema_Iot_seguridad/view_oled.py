# view_oled.py - Manejo de la pantalla OLED SSD1306 en Pico W
from machine import Pin, I2C
import ssd1306

class OLEDView:
    def __init__(self, sda_pin=0, scl_pin=1):
        self.display = None
        try:
            i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=400000)
            self.display = ssd1306.SSD1306_I2C(128, 64, i2c)
            self.clear()
        except Exception as e:
            print("Error inicializando pantalla OLED:", e)

    def clear(self):
        if self.display:
            self.display.fill(0)
            self.display.show()

    def update_status(self, armed, alarm, distance, motion):
        if not self.display:
            return

        self.display.fill(0)
        self.display.text("== PICO W SEC ==", 0, 0)

        # Estado del sistema
        if armed:
            self.display.text("ESTADO: ARMADO", 0, 16)
        else:
            self.display.text("ESTADO: DESARMADO", 0, 16)

        # Alerta
        if alarm:
            self.display.text("!! ALARMA ACTIVA !!", 0, 30)
        else:
            self.display.text("ALARM: NORMAL", 0, 30)

        # Variables de Sensores
        self.display.text("Dist: {:.1f} cm".format(distance), 0, 44)
        self.display.text("PIR: {}".format("MOV!" if motion else "OK"), 0, 54)

        self.display.show()
