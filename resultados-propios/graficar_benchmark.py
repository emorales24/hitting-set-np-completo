import csv
import os
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
os.environ.setdefault("MPLCONFIGDIR", str(BASE / ".matplotlib-cache"))

import matplotlib.pyplot as plt

ESTILO = "Solarize_Light2"
TIPOS = ["facil", "aleatorio", "dificil"]

# Paleta Okabe-Ito: suele funcionar mejor para daltonismo.
COLORES = {
    "facil": "#0072B2",
    "aleatorio": "#E69F00",
    "dificil": "#D55E00",
    "bt": "#0072B2",
    "greedy": "#E69F00",
    "pl": "#009E73",
    "aprox_lp": "#CC79A7",
}

MARCADORES = {
    "facil": "o",
    "aleatorio": "s",
    "dificil": "^",
    "bt": "o",
    "greedy": "s",
    "pl": "^",
    "aprox_lp": "D",
}

LINEAS = {
    "facil": "-",
    "aleatorio": "--",
    "dificil": "-.",
    "bt": "-",
    "greedy": "--",
    "pl": "-.",
    "aprox_lp": ":",
}


def cargar_resultados(ruta_csv):
    filas = []

    with ruta_csv.open("r", encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo)
        columnas = set(reader.fieldnames or [])
        requeridas = {
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
        }
        faltantes = requeridas - columnas
        if faltantes:
            raise SystemExit(
                "El csv tiene formato viejo o incompleto. "
                "Ejecuta primero: python3 mediciones.py"
            )

        for fila in reader:
            tiempo = (fila.get("tiempo_promedio") or "").strip()
            if not tiempo:
                continue

            ratio = (fila.get("ratio") or "").strip()
            filas.append(
                {
                    "archivo": fila["archivo"],
                    "experimento": fila["experimento"],
                    "tipo": fila["tipo"],
                    "algoritmo": fila["algoritmo"],
                    "n": int(fila["n"]),
                    "m": int(fila["m"]),
                    "solucion_tam": int(fila["solucion_tam"]),
                    "optimo": int(fila["optimo"]) if fila.get("optimo") else None,
                    "ratio": float(ratio) if ratio else None,
                    "tiempo_promedio": float(tiempo),
                }
            )

    return filas


def filtrar(filas, **condiciones):
    resultado = []
    for fila in filas:
        coincide = True
        for clave, valor in condiciones.items():
            if fila.get(clave) != valor:
                coincide = False
                break
        if coincide:
            resultado.append(fila)
    return resultado


def puntos_por_serie(filas, serie, eje_x, eje_y):
    grupos = defaultdict(list)
    for fila in filas:
        grupos[fila[serie]].append((fila[eje_x], fila[eje_y]))

    resultado = {}
    for nombre, puntos in grupos.items():
        puntos.sort(key=lambda punto: punto[0])
        resultado[nombre] = puntos
    return resultado


def aplicar_estilo():
    plt.style.use(ESTILO)
    plt.rcParams["figure.figsize"] = (9, 5.5)
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.35


def graficar_series(filas, serie, eje_x, eje_y, titulo, xlabel, ylabel, salida_png):
    aplicar_estilo()
    series = puntos_por_serie(filas, serie, eje_x, eje_y)

    plt.figure()
    for nombre in sorted(series):
        puntos = series[nombre]
        xs = [x for x, _ in puntos]
        ys = [y for _, y in puntos]
        plt.plot(
            xs,
            ys,
            color=COLORES.get(nombre),
            linestyle=LINEAS.get(nombre, "-"),
            marker=MARCADORES.get(nombre, "o"),
            linewidth=2.2,
            markersize=6,
            label=nombre,
        )

    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.yscale("log")
    plt.legend()
    plt.tight_layout()
    plt.savefig(salida_png, dpi=160)
    plt.close()


def graficar_ratio(filas, salida_png):
    aplicar_estilo()

    # El ratio viene de mediciones.py: |C_algoritmo| / |C_optimo|.
    # Sirve para ver que tan lejos queda cada algoritmo del optimo.
    series = puntos_por_serie(filas, "algoritmo", "n", "ratio")

    plt.figure()
    for algoritmo in sorted(series):
        puntos = [(x, y) for x, y in series[algoritmo] if y is not None]
        if not puntos:
            continue
        xs = [x for x, _ in puntos]
        ys = [y for _, y in puntos]
        plt.plot(
            xs,
            ys,
            color=COLORES.get(algoritmo),
            linestyle=LINEAS.get(algoritmo, "-"),
            marker=MARCADORES.get(algoritmo, "o"),
            linewidth=2.2,
            markersize=6,
            label=algoritmo,
        )

    plt.axhline(1, color="gray", linewidth=1, linestyle="--")
    plt.title("Aproximación a la solución por algoritmo")
    plt.xlabel("Cantidad de jugadores (n), con m = 2n")
    plt.ylabel("|C_algoritmo| / |C_optimo|")
    plt.legend()
    plt.tight_layout()
    plt.savefig(salida_png, dpi=160)
    plt.close()


def main():
    csv_path = BASE / "resultados_mediciones.csv"

    if not csv_path.exists():
        raise SystemExit(
            f"No se encontro el benchmark en: {csv_path}. Ejecuta mediciones.py primero."
        )

    filas = cargar_resultados(csv_path)
    if not filas:
        raise SystemExit("No hay filas validas con tiempo para graficar.")

    bt_varia_n = filtrar(filas, algoritmo="bt", experimento="varia_n")
    bt_varia_m = filtrar(filas, algoritmo="bt", experimento="varia_m")
    bt_crecen = filtrar(filas, algoritmo="bt", experimento="crecen_juntos")

    comparacion_algoritmos = [
        fila
        for fila in filas
        if fila["experimento"] == "crecen_juntos" and fila["tipo"] == "aleatorio"
    ]

    salidas = [
        (
            bt_varia_n,
            "tipo",
            "n",
            "tiempo_promedio",
            "BT variando n, con m fijo",
            "Cantidad de jugadores (n), con m = 60",
            "Tiempo promedio (segundos)",
            BASE / "bt_varia_n_m_fijo.png",
        ),
        (
            bt_varia_m,
            "tipo",
            "m",
            "tiempo_promedio",
            "BT variando m, con n fijo",
            "Cantidad de pedidos (m), con n = 40",
            "Tiempo promedio (segundos)",
            BASE / "bt_varia_m_n_fijo.png",
        ),
        (
            bt_crecen,
            "tipo",
            "n",
            "tiempo_promedio",
            "BT con n y m creciendo juntos",
            "Cantidad de jugadores (n), con m = 2n",
            "Tiempo promedio (segundos)",
            BASE / "bt_crecen_juntos.png",
        ),
        (
            comparacion_algoritmos,
            "algoritmo",
            "n",
            "tiempo_promedio",
            "Tiempo por algoritmo en instancias aleatorias",
            "Cantidad de jugadores (n), con m = 2n",
            "Tiempo promedio (segundos)",
            BASE / "comparacion_tiempos_algoritmos.png",
        ),
    ]

    for args in salidas:
        graficar_series(*args)
        print(f"Grafico listo: {args[-1]}")

    salida_ratio = BASE / "comparacion_aproximacion_algoritmos.png"
    graficar_ratio(comparacion_algoritmos, salida_ratio)
    print(f"Grafico listo: {salida_ratio}")


if __name__ == "__main__":
    main()
