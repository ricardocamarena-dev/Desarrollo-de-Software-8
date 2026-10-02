from funciones_auxiliares import FuncionesAuxiliares


class MostrarDatos:
    def __init__(self, parqueo, ocupacion_estado, funciones_aux):
        self.parqueo = parqueo
        self.ocupacion_estado = ocupacion_estado
        self.funciones = funciones_aux

    def mostrar_autos_dentro(self):
        print("\nAutos dentro del parqueo:")
        if not self.parqueo.placas_estacionadas:
            print("  (ninguno)")
        for i, placa in enumerate(self.parqueo.placas_estacionadas, start=1):
            print(f"  {i}. {placa} (entro a las "
                  f"{self.funciones.formatear_hora(self.parqueo.entradas_activas[placa])})")

    def mostrar_historial_auto(self):
        placa = input("Placa a consultar (ej. ABC-123): ").strip().upper()
        if placa not in self.parqueo.historial:
            print("  Esa placa no tiene eventos registrados.")
            return
        print(f"\nHistorial de {placa}:")
        for _, hora, tarifa in self.parqueo.historial[placa]:
            print(f"  {hora}  tarifa: ${tarifa:.2f}")

    def mostrar_todos_los_eventos(self):
        print("\nTodos los eventos (placa, hora, tarifa):")
        if not self.parqueo.eventos:
            print("  (sin eventos)")
        for evento in self.parqueo.eventos:
            print(f"  {evento}")

    def registrar_placa_manual(self, eventos):
        placa = input("Placa del auto (ej. ABC-123): ").strip().upper()
        if not placa:
            print("  Error: la placa no puede estar vacia.")
            return
        eventos.entrar_auto(placa)