def cargar_pedidos_de_ruta(ruta):
    """
    Lee una instancia desde un txt.

    Formato:
    - cada linea es un pedido de la prensa, o sea un B_i
    - en cada linea los jugadores vienen separados por coma

    Devuelve:
    - jugadores: set con todos los jugadores, o sea A
    - pedidos: lista de sets, o sea B_1, B_2, ..., B_m
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
