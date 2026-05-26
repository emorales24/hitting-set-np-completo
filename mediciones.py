import time
import os
import csv

from cargador_pedidos import cargar_pedidos_de_ruta
from hitting_set_bt import hitting_set_backtracking
from validador_polinomial import validar_cobertura
from generador_datos import generar_sets_completos


REPETICIONES = 3
TIMEOUT_SEGUNDOS = 120


def medir_tiempo(jugadores, pedidos):
    """
    Mide el tiempo de ejecución del backtracking.
    Ejecuta varias veces y devuelve el promedio.

    Parámetros:
        jugadores: set con todos los jugadores.
        pedidos: lista de sets con los pedidos.

    Devuelve:
        tupla (solucion, tiempo_promedio, tiempos) o (None, None, None) si excede el timeout.
    """
    tiempos = []
    solucion = None

    for i in range(REPETICIONES):
        inicio = time.time()
        resultado = hitting_set_backtracking(jugadores, pedidos)
        fin = time.time()

        duracion = fin - inicio
        tiempos.append(duracion)
        solucion = resultado

        # Si una sola ejecución supera el timeout, no repetimos
        if duracion > TIMEOUT_SEGUNDOS:
            return None, None, None

    tiempo_promedio = sum(tiempos) / len(tiempos)
    return solucion, tiempo_promedio, tiempos


def medir_archivos_catedra():
    """
    Ejecuta mediciones sobre los archivos de la cátedra.
    Devuelve una lista de diccionarios con los resultados.
    """
    directorio = "archivos-test-catedra"
    archivos = [
        "5.txt", "7.txt", "10_pocos.txt", "10_varios.txt", "10_todos.txt",
        "15.txt", "20.txt", "50.txt", "75.txt", "100.txt", "200.txt"
    ]

    resultados_esperados = {
        "5.txt": 2, "7.txt": 2, "10_pocos.txt": 3, "10_varios.txt": 6,
        "10_todos.txt": 10, "15.txt": 4, "20.txt": 5, "50.txt": 6,
        "75.txt": 8, "100.txt": 9, "200.txt": 9
    }

    resultados = []

    print("=" * 70)
    print("MEDICIONES - ARCHIVOS DE LA CÁTEDRA")
    print("=" * 70)

    for archivo in archivos:
        ruta = os.path.join(directorio, archivo)
        jugadores, pedidos = cargar_pedidos_de_ruta(ruta)

        solucion, tiempo_prom, tiempos = medir_tiempo(jugadores, pedidos)

        if solucion is None:
            print(f"{archivo}: TIMEOUT (>{TIMEOUT_SEGUNDOS}s)")
            continue

        es_valida = validar_cobertura(solucion, jugadores, pedidos)
        esperado = resultados_esperados.get(archivo, "?")
        cantidad_ok = len(solucion) == esperado

        estado = "OK" if (es_valida and cantidad_ok) else "FALLO"

        print(f"{archivo:20s} | n={len(jugadores):4d} | m={len(pedidos):4d} | "
              f"|C|={len(solucion):3d} (esperado {esperado}) | "
              f"t={tiempo_prom:.6f}s | {estado}")

        resultados.append({
            "archivo": archivo,
            "tipo": "catedra",
            "n": len(jugadores),
            "m": len(pedidos),
            "solucion_tam": len(solucion),
            "esperado": esperado,
            "tiempo_promedio": tiempo_prom,
            "valida": es_valida,
            "correcta": cantidad_ok
        })

    return resultados


def medir_archivos_propios():
    """
    Genera los sets propios y ejecuta mediciones sobre ellos.
    Devuelve una lista de diccionarios con los resultados.
    """
    directorio = "archivos-test-propios"
    sets_info = generar_sets_completos(directorio)

    resultados = []

    print()
    print("=" * 70)
    print("MEDICIONES - ARCHIVOS PROPIOS")
    print("=" * 70)

    for nombre, n, m, tipo in sets_info:
        ruta = os.path.join(directorio, nombre)
        jugadores, pedidos = cargar_pedidos_de_ruta(ruta)

        solucion, tiempo_prom, tiempos = medir_tiempo(jugadores, pedidos)

        if solucion is None:
            print(f"{nombre:25s} | n={n:4d} | m={m:4d} | TIMEOUT (>{TIMEOUT_SEGUNDOS}s)")
            resultados.append({
                "archivo": nombre,
                "tipo": tipo,
                "n": n,
                "m": m,
                "solucion_tam": None,
                "tiempo_promedio": None,
                "valida": None,
            })
            continue

        es_valida = validar_cobertura(solucion, jugadores, pedidos)

        print(f"{nombre:25s} | n={n:4d} | m={m:4d} | "
              f"|C|={len(solucion):3d} | "
              f"t={tiempo_prom:.6f}s | "
              f"valida={es_valida} | tipo={tipo}")

        resultados.append({
            "archivo": nombre,
            "tipo": tipo,
            "n": n,
            "m": m,
            "solucion_tam": len(solucion),
            "tiempo_promedio": tiempo_prom,
            "valida": es_valida,
        })

    return resultados


def guardar_resultados_csv(resultados, ruta_csv):
    """
    Guarda los resultados de las mediciones en un archivo CSV.
    """
    if not resultados:
        return

    campos = list(resultados[0].keys())

    with open(ruta_csv, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for fila in resultados:
            escritor.writerow(fila)

    print(f"\nResultados guardados en: {ruta_csv}")


def main():
    todos_los_resultados = []

    resultados_catedra = medir_archivos_catedra()
    todos_los_resultados.extend(resultados_catedra)

    resultados_propios = medir_archivos_propios()
    todos_los_resultados.extend(resultados_propios)

    print()
    print("=" * 70)
    print("RESUMEN")
    print("=" * 70)

    total = len(todos_los_resultados)
    validos = sum(1 for r in todos_los_resultados if r.get("valida") is True)
    timeouts = sum(1 for r in todos_los_resultados if r.get("tiempo_promedio") is None)

    print(f"Total de instancias: {total}")
    print(f"Soluciones válidas:  {validos}")
    print(f"Timeouts:            {timeouts}")

    guardar_resultados_csv(todos_los_resultados, "resultados_mediciones_bt.csv")


if __name__ == "__main__":
    main()