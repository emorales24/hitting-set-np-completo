from pathlib import Path


def cargar_pedidos_de_ruta(ruta):
    """
    Lee una instancia del problema desde un archivo de texto.

    Formato:
    - Cada linea es un pedido de la prensa (ie. un subconjunto B_i).
    - En cada linea, los jugadores estan separados por coma.

    Devuelve:
    - set de jugadores (ie. el conjunto A).
    - los pedidos en una lista de sets (ie. los B_1, B_2, ..., B_m).
    """

    pedidos = []
    jugadores = set()

    with open(ruta, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                continue

            pedido = set()

            for jugador in linea.split(","):
                jugador = jugador.strip()
                if jugador:
                    pedido.add(jugador)
                    jugadores.add(jugador)

            if pedido:
                pedidos.append(pedido)

    return jugadores, pedidos
