from parqueo import CAPACIDAD_MAXIMA, UMBRAL_MEDIO


class OcupacionEstado:
    def __init__(self, parqueo):
        self.parqueo = parqueo

    def espacios_libres(self):
        return self.parqueo.espacios_libres()

    def calcular_ocupacion(self):
        return len(self.parqueo.placas_estacionadas) / CAPACIDAD_MAXIMA * 100

    def estado_parqueo(self):
        porcentaje = self.calcular_ocupacion()
        if porcentaje >= 100:
            return "LLENO"
        elif porcentaje >= UMBRAL_MEDIO:
            return "MEDIO OCUPADO"
        else:
            return "DISPONIBLE"

    def mostrar_resumen(self):
        print(f"\n  Ocupacion: {self.calcular_ocupacion():.1f}%  |  "
              f"Estado: {self.estado_parqueo()}")
        print(f"  Espacios libres: {self.espacios_libres()} de {CAPACIDAD_MAXIMA}")