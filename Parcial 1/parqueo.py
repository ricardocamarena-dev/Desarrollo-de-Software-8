CAPACIDAD_MAXIMA = 20
TARIFA_POR_MEDIA_HORA = 0.75
UMBRAL_MEDIO = 50
MINUTOS_POR_CICLO = 30


class Parqueo:
    def __init__(self):
        self.placas_estacionadas = []
        self.entradas_activas = {}
        self.eventos = []
        self.historial = {}
        self.reloj = 8 * 60

    def espacios_libres(self):
        return CAPACIDAD_MAXIMA - len(self.placas_estacionadas)