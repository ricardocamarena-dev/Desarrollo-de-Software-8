# Sistema de Parqueo Inteligente

Examen Parcial #1 - Desarrollo de Software 8
Universidad Tecnológica de Panamá (UTP) - Facultad de Sistemas Computacionales

## Grupo

**Integrantes:**
1. Alexander Toribio 8-994-2483
2. Kristel Ortega 
3. Luis 
4. Ricardo Camarena 8-910-282
5. M

## Descripción

Simulación en Python de un sistema de parqueo para un centro comercial. Genera autos con placas aleatorias, calcula la ocupación, cobra tarifa por hora y guarda el historial de cada auto.

## Requisitos

- Python 3.8 o superior (solo usa librerías estándar: `random`, `string`, `math`).

## Uso

Al iniciar aparece un menú:

| Opción | Acción |
|--------|--------|
| 1 | Simular un ciclo manual (el usuario indica cuántos autos entran y salen) |
| 2 | Simular varios ciclos aleatorios |
| 3 | Registrar la entrada de un auto con placa propia |
| 4 | Ver los autos que están dentro |
| 5 | Ver el historial de una placa |
| 6 | Ver todos los eventos registrados |
| 7 | Ver ocupación y espacios libres |
| 0 | Salir |

## Configuración

Las constantes están al inicio de `parqueo.py`: `CAPACIDAD_MAXIMA` (20), `TARIFA_POR_HORA` (1.50), `UMBRAL_MEDIO` (50 %) y `MINUTOS_POR_CICLO` (30).

## Estados del parqueo

- **DISPONIBLE:** menos del 50 % de ocupación
- **MEDIO OCUPADO:** entre 50 % y 99 %
- **LLENO:** 100 %

## Estructuras de datos

- **Lista** `placas_estacionadas`: autos dentro en este momento.
- **Tuplas** `(placa, hora, tarifa)`: cada evento de entrada (tarifa 0.00) o salida (tarifa cobrada).
- **Diccionario** `historial`: clave = placa, valor = lista de sus eventos.
