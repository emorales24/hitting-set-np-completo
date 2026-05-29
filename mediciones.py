import csv
import os
import time

from cargador_pedidos import cargar_pedidos_de_ruta
from generador_datos import generar_benchmarks_controlados
from hitting_set_aprox import hitting_set_aprox_lp
from hitting_set_bt import hitting_set_backtracking
from hitting_set_greedy import hitting_set_greedy
from hitting_set_pl import hitting_set_pl
from validador_polinomial import validar_cobertura

REPETICIONES = 3
TIMEOUT_SEGUNDOS = 120


def medir_algoritmo(nombre_algoritmo, algoritmo, jugadores, pedidos):
    """
    Mide un algoritmo varias veces y devuelve la solucion y el tiempo promedio.
    """
    tiempos = []
    solucion = None

    for _ in range(REPETICIONES):
        inicio = time.time()
        resultado = algoritmo(jugadores, pedidos)
        fin = time.time()

        duracion = fin - inicio
        tiempos.append(duracion)
        solucion = resultado

        if duracion > TIMEOUT_SEGUNDOS:
            return None, None

    tiempo_promedio = sum(tiempos) / len(tiempos)
    return solucion, tiempo_promedio


def armar_fila(info, algoritmo, solucion, tiempo_promedio, jugadores, pedidos, optimo):
    """
    Arma una fila comun para todos los algoritmos.
    """
    valida = solucion is not None and validar_cobertura(solucion, jugadores, pedidos)
    solucion_tam = len(solucion) if solucion is not None else None

    # Mide la calidad contra el optimo: 1 es optimo, mas grande es peor.
    ratio = None
    if solucion_tam is not None and optimo:
        ratio = solucion_tam / optimo

    return {
        "archivo": info["archivo"],
        "experimento": info["experimento"],
        "tipo": info["tipo"],
        "algoritmo": algoritmo,
        "n": info["n"],
        "m": info["m"],
        "solucion_tam": solucion_tam,
        "optimo": optimo,
        "ratio": ratio,
        "tiempo_promedio": tiempo_promedio,
        "valida": valida,
    }


def medir_benchmarks_controlados():
    """
    Genera los benchmarks controlados y los mide.

    Para bt se miden todos los experimentos:
    - varia_n
    - varia_m
    - crecen_juntos

    Para comparar algoritmos se usa solo crecen_juntos, asi no salen
    demasiados graficos ni se mezclan demasiadas historias.
    """
    directorio = "archivos-test-propios"
    sets_info = generar_benchmarks_controlados(directorio)

    algoritmos_extra = {
        "greedy": hitting_set_greedy,
        "pl": hitting_set_pl,
        "aprox_lp": lambda jugadores, pedidos: hitting_set_aprox_lp(jugadores, pedidos)[
            0
        ],
    }

    resultados = []

    print("=" * 80)
    print("MEDICIONES CONTROLADAS")
    print("=" * 80)

    for info in sets_info:
        ruta = os.path.join(directorio, info["archivo"])
        jugadores, pedidos = cargar_pedidos_de_ruta(ruta)

        solucion_bt, tiempo_bt = medir_algoritmo(
            "bt", hitting_set_backtracking, jugadores, pedidos
        )
        optimo = len(solucion_bt) if solucion_bt is not None else None

        resultados.append(
            armar_fila(info, "bt", solucion_bt, tiempo_bt, jugadores, pedidos, optimo)
        )

        print(
            f"{info['archivo']:38s} | bt | "
            f"n={info['n']:3d} | m={info['m']:3d} | "
            f"opt={optimo} | t={tiempo_bt}"
        )

        if info["experimento"] != "crecen_juntos":
            continue

        for nombre_algoritmo, algoritmo in algoritmos_extra.items():
            solucion, tiempo_promedio = medir_algoritmo(
                nombre_algoritmo, algoritmo, jugadores, pedidos
            )
            resultados.append(
                armar_fila(
                    info,
                    nombre_algoritmo,
                    solucion,
                    tiempo_promedio,
                    jugadores,
                    pedidos,
                    optimo,
                )
            )
            solucion_tam = len(solucion) if solucion is not None else None
            print(
                f"{info['archivo']:38s} | {nombre_algoritmo:8s} | "
                f"|C|={solucion_tam} | t={tiempo_promedio}"
            )

    return resultados


def guardar_resultados_csv(resultados, ruta_csv):
    """
    Guarda las mediciones en un csv.
    """
    if not resultados:
        return

    os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)

    campos = [
        "archivo",
        "experimento",
        "tipo",
        "algoritmo",
        "n",
        "m",
        "solucion_tam",
        "optimo",
        "ratio",
        "tiempo_promedio",
        "valida",
    ]

    with open(ruta_csv, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for fila in resultados:
            escritor.writerow(fila)

    print(f"\nResultados guardados en: {ruta_csv}")


def main():
    resultados = medir_benchmarks_controlados()

    total = len(resultados)
    validos = sum(1 for fila in resultados if fila.get("valida") is True)
    timeouts = sum(1 for fila in resultados if fila.get("tiempo_promedio") is None)

    print()
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"Total de mediciones: {total}")
    print(f"Soluciones validas:  {validos}")
    print(f"Timeouts:            {timeouts}")

    guardar_resultados_csv(resultados, "resultados-propios/resultados_mediciones.csv")


if __name__ == "__main__":
    main()
