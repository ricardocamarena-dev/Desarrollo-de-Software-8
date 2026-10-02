from parqueo import Parqueo
from funciones_auxiliares import FuncionesAuxiliares
from ocupacion_estado import OcupacionEstado
from eventos import Eventos
from ciclo_simulacion import CicloSimulacion
from mostrar_datos import MostrarDatos


def main():
    parqueo = Parqueo()
    funciones_aux = FuncionesAuxiliares()
    ocupacion_estado = OcupacionEstado(parqueo)
    eventos = Eventos(parqueo, funciones_aux)
    ciclo = CicloSimulacion(parqueo, eventos, ocupacion_estado, funciones_aux)
    mostrar = MostrarDatos(parqueo, ocupacion_estado, funciones_aux)

    opciones = {
        "1": ("Simular ciclo manual", ciclo.simulacion_manual),
        "2": ("Simular ciclos aleatorios", ciclo.simulacion_aleatoria),
        "3": ("Registrar entrada de carro", lambda: mostrar.registrar_placa_manual(eventos)),
        "4": ("Registrar salida de auto", lambda: eventos.salir_auto(input("Placa a sacar: ").strip().upper())),
        "5": ("Ver historial de un auto", mostrar.mostrar_historial_auto),
        "6": ("Ver todos los eventos", mostrar.mostrar_todos_los_eventos),
        "7": ("Ver estado del parqueo", ocupacion_estado.mostrar_resumen),
        "8": ("Ver autos dentro", mostrar.mostrar_autos_dentro),
    }

    while True:
        print("\n===== PARQUEO INTELIGENTE =====")
        for clave, (texto, _) in opciones.items():
            print(f"{clave}. {texto}")
        print("0. Salir")
        eleccion = input("Elija una opcion: ").strip()
        if eleccion == "0":
            print("Hasta luego.")
            break
        elif eleccion in opciones:
            opciones[eleccion][1]()
        else:
            print("  Error: opcion no valida.")


if __name__ == "__main__":
    main()