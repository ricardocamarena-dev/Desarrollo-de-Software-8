import random
from funciones_auxiliares import FuncionesAuxiliares


class CicloSimulacion:
    def __init__(self, parqueo, eventos, ocupacion_estado, funciones_aux):
        self.parqueo = parqueo
        self.eventos = eventos
        self.ocupacion_estado = ocupacion_estado
        self.funciones = funciones_aux

    def ciclo_simulacion(self, entran, salen):
        print(f"\n--- Ciclo a las {self.funciones.formatear_hora(self.parqueo.reloj)} ---")

        if salen > len(self.parqueo.placas_estacionadas):
            print(f"  Aviso: solo hay {len(self.parqueo.placas_estacionadas)} autos dentro; "
                  f"saldran solo esos.")
            salen = len(self.parqueo.placas_estacionadas)
        if entran > self.ocupacion_estado.espacios_libres() + salen:
            print(f"  Aviso: solo caben {self.ocupacion_estado.espacios_libres() + salen} autos; "
                  f"entraran solo esos.")
            entran = self.ocupacion_estado.espacios_libres() + salen

        for _ in range(salen):
            self.eventos.salir_auto()
        for _ in range(entran):
            self.eventos.entrar_auto()

        self.parqueo.reloj += 30
        self.ocupacion_estado.mostrar_resumen()

    def simulacion_manual(self):
        while True:
            entran = self.funciones.pedir_entero("Cuantos autos entran en este ciclo? ")
            salen = self.funciones.pedir_entero("Cuantos autos salen en este ciclo? ")
            if salen > len(self.parqueo.placas_estacionadas):
                print(f"  Error: solo hay {len(self.parqueo.placas_estacionadas)} autos dentro.")
                print(f"  No pueden salir {salen} autos. Intente de nuevo.")
                continue
            break
        self.ciclo_simulacion(entran, salen)

    def simulacion_aleatoria(self):
        ciclos = self.funciones.pedir_entero("Cuantos ciclos desea simular? ")
        for _ in range(ciclos):
            self.ciclo_simulacion(random.randint(0, 5), random.randint(0, 5))