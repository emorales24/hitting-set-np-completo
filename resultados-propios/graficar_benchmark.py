import csv
from collections import defaultdict
from pathlib import Path

try:
    import matplotlib.pyplot as plt
except ImportError as exc:  # pragma: no cover - depende del entorno
    raise SystemExit(
        "Falta matplotlib. Instalalo para poder generar los graficos del benchmark."
    ) from exc


def cargar_resultados(ruta_csv):
    with ruta_csv.open("r", encoding="utf-8", newline="") as archivo:
        reader = csv.DictReader(archivo)
        filas = []
        for fila in reader:
            tiempo_str = (fila.get("tiempo_promedio") or "").strip()
            if not tiempo_str:
                # Timeout o fila incompleta: no se grafica.
                continue

            filas.append(
                {
                    "archivo": fila.get("archivo", ""),
                    "n": int(fila["n"]),
                    "m": int(fila["m"]),
                    "tiempo_promedio": float(tiempo_str),
                }
            )

    filas.sort(key=lambda x: (x["n"], x["m"]))
    return filas


def agrupar_por_tamanio(filas):
    grupos = defaultdict(list)
    for fila in filas:
        grupos[(fila["n"], fila["m"])].append(fila["tiempo_promedio"])

    resultado = []
    for (n, m), tiempos in grupos.items():
        promedio = sum(tiempos) / len(tiempos)
        resultado.append(
            {
                "n": n,
                "m": m,
                "tiempo_promedio": promedio,
                "repeticiones": len(tiempos),
            }
        )

    resultado.sort(key=lambda x: (x["n"], x["m"]))
    return resultado


def promediar_por_eje(filas_agrupadas, clave):
    acumulado = defaultdict(list)
    for fila in filas_agrupadas:
        acumulado[fila[clave]].append(fila["tiempo_promedio"])

    xs = sorted(acumulado)
    ys = [sum(acumulado[x]) / len(acumulado[x]) for x in xs]
    return xs, ys


def graficar_tiempo_por_n(filas, salida_png):
    filas_agrupadas = agrupar_por_tamanio(filas)
    tamanios, tiempos = promediar_por_eje(filas_agrupadas, "n")

    plt.figure(figsize=(9, 5.5))
    plt.plot(tamanios, tiempos, marker="o", linewidth=1.8)
    plt.title("TP3 BT: tiempo promedio segun cantidad de jugadores")
    plt.xlabel("Cantidad de jugadores (n)")
    plt.ylabel("Tiempo promedio (segundos)")
    plt.yscale("log")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(salida_png, dpi=160)
    plt.close()


def graficar_tiempo_por_m(filas, salida_png):
    filas_agrupadas = agrupar_por_tamanio(filas)
    pedidos, tiempos = promediar_por_eje(filas_agrupadas, "m")

    plt.figure(figsize=(9, 5.5))
    plt.plot(pedidos, tiempos, marker="o", linewidth=1.8)
    plt.title("TP3 BT: tiempo promedio segun cantidad de pedidos")
    plt.xlabel("Cantidad de pedidos (m)")
    plt.ylabel("Tiempo promedio (segundos)")
    plt.yscale("log")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(salida_png, dpi=160)
    plt.close()


def graficar_loglog(filas, salida_png):
    filas_agrupadas = agrupar_por_tamanio(filas)
    tamanios, tiempos = promediar_por_eje(filas_agrupadas, "n")

    plt.figure(figsize=(9, 5.5))
    plt.loglog(tamanios, tiempos, marker="o", linewidth=1.8)
    plt.title("TP3 BT: escala log-log segun cantidad de jugadores")
    plt.xlabel("Cantidad de jugadores (n)")
    plt.ylabel("Tiempo promedio (segundos)")
    plt.grid(True, which="both", alpha=0.3)
    plt.tight_layout()
    plt.savefig(salida_png, dpi=160)
    plt.close()


def graficar_tiempo_ordenado_por_tamanio(filas, salida_png):
    filas_agrupadas = agrupar_por_tamanio(filas)
    puntos_ordenados = sorted(
        filas_agrupadas, key=lambda x: x["tiempo_promedio"]
    )
    posiciones = list(range(1, len(puntos_ordenados) + 1))
    tiempos = [fila["tiempo_promedio"] for fila in puntos_ordenados]

    plt.figure(figsize=(9, 5.5))
    plt.plot(posiciones, tiempos, marker="o", linewidth=1.8)
    plt.title("TP3 BT: tiempos por tamanio ordenados de menor a mayor")
    plt.xlabel("Indice de instancia (agrupada por tamanio n,m)")
    plt.ylabel("Tiempo promedio (segundos)")
    plt.yscale("log")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(salida_png, dpi=160)
    plt.close()


def main():
    base = Path(__file__).resolve().parent
    csv_path = base / "resultados_mediciones_bt.csv"

    if not csv_path.exists():
        raise SystemExit(
            f"No se encontro el benchmark en: {csv_path}. "
            "Ejecuta mediciones.py primero."
        )

    filas = cargar_resultados(csv_path)
    if not filas:
        raise SystemExit("No hay filas validas con tiempo para graficar.")

    salida_por_n = base / "grafico_tiempo_por_n.png"
    salida_por_m = base / "grafico_tiempo_por_m.png"
    salida_loglog = base / "grafico_tiempo_loglog.png"
    salida_ordenado = base / "grafico_tiempo_ordenado_por_tamanio.png"

    graficar_tiempo_por_n(filas, salida_por_n)
    graficar_tiempo_por_m(filas, salida_por_m)
    graficar_loglog(filas, salida_loglog)
    graficar_tiempo_ordenado_por_tamanio(filas, salida_ordenado)

    print(f"Grafico listo: {salida_por_n}")
    print(f"Grafico listo: {salida_por_m}")
    print(f"Grafico listo: {salida_loglog}")
    print(f"Grafico listo: {salida_ordenado}")


if __name__ == "__main__":
    main()
