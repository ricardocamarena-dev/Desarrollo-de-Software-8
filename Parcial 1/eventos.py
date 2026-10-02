import random
from funciones_auxiliares import FuncionesAuxiliares


class Eventos:
    def __init__(self, parqueo, funciones_aux):
        self.parqueo = parqueo
        self.funciones = funciones_aux

    def registrar_evento(self, placa, tarifa):
        evento = (placa, self.funciones.formatear_hora(self.parqueo.reloj), tarifa)
        self.parqueo.eventos.append(evento)
        self.parqueo.historial.setdefault(placa, []).append(evento)

    def entrar_auto(self, placa=None):
        if self.parqueo.espacios_libres() == 0:
            print("  Parqueo lleno: no puede entrar mas autos.")
            return False
        if placa is None:
            placa = self.funciones.generar_placa(self.parqueo.placas_estacionadas)
        if placa in self.parqueo.placas_estacionadas:
            print(f"  Error: el auto {placa} ya esta dentro.")
            return False
        self.parqueo.placas_estacionadas.append(placa)
        self.parqueo.entradas_activas[placa] = self.parqueo.reloj
        self.registrar_evento(placa, 0.0)
        print(f"  ENTRADA  {placa} a las {self.funciones.formatear_hora(self.parqueo.reloj)}")
        return True

    def salir_auto(self, placa=None):
        if not self.parqueo.placas_estacionadas:
            print("  El parqueo esta vacio: no hay autos que salgan.")
            return False
        if placa is None:
            placa = random.choice(self.parqueo.placas_estacionadas)
        if placa not in self.parqueo.placas_estacionadas:
            print(f"  Error: el auto {placa} no esta en el parqueo.")
            return False
        tiempo = self.parqueo.reloj - self.parqueo.entradas_activas.pop(placa)
        tarifa = self.funciones.calcular_tarifa(tiempo)
        self.parqueo.placas_estacionadas.remove(placa)
        self.registrar_evento(placa, tarifa)
        print(f"  SALIDA   {placa} a las {self.funciones.formatear_hora(self.parqueo.reloj)} "
              f"-> paga ${tarifa:.2f}")
        return True