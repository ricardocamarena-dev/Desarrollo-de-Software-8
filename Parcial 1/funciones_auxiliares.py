import random
import string
import math


class FuncionesAuxiliares:
    @staticmethod
    def formatear_hora(minutos):
        minutos = minutos % (24 * 60)
        return f"{minutos // 60:02d}:{minutos % 60:02d}"

    @staticmethod
    def generar_placa(placas_existentes):
        while True:
            letras = "".join(random.choices(string.ascii_uppercase, k=3))
            numeros = "".join(random.choices(string.digits, k=3))
            placa = f"{letras}-{numeros}"
            if placa not in placas_existentes:
                return placa

    @staticmethod
    def pedir_entero(mensaje):
        while True:
            try:
                valor = int(input(mensaje))
                if valor < 0:
                    print("  Error: el numero no puede ser negativo.")
                    continue
                return valor
            except ValueError:
                print("  Error: debe ingresar un numero entero.")

    @staticmethod
    def calcular_tarifa(minutos_dentro, tarifa_por_media_hora=0.75):
        medias_horas = max(1, math.ceil(minutos_dentro / 30))
        return medias_horas * tarifa_por_media_hora