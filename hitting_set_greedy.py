def hitting_set_greedy(jugadores, pedidos):
    """
    Heurística greedy para el Hitting Set Problem.

    Estrategia: en cada paso, elegir el jugador que cubre
    la mayor cantidad de pedidos aún no cubiertos.
    Repetir hasta que todos los pedidos estén cubiertos.

    Esta es una O(log m)-aproximación, análoga a la
    aproximación greedy clásica de Set Cover.

    Complejidad: O(n * m) por iteración, y a lo sumo n iteraciones,
    dando O(n^2 * m) en el peor caso. En la práctica es mucho menor
    porque la cantidad de iteraciones es |C| (tamaño de la solución).

    Parámetros:
        jugadores: set con todos los jugadores (A).
        pedidos: lista de sets, donde cada set es un pedido (B_i).

    Devuelve:
        set con los jugadores elegidos.
    """
    solucion = set()
    pedidos_restantes = list(pedidos)

    while len(pedidos_restantes) > 0:
        mejor_jugador = _jugador_que_mas_cubre(jugadores, pedidos_restantes)
        solucion.add(mejor_jugador)

        # Filtrar los pedidos que este jugador cubre
        pedidos_sin_cubrir = []
        for pedido in pedidos_restantes:
            if mejor_jugador not in pedido:
                pedidos_sin_cubrir.append(pedido)
        pedidos_restantes = pedidos_sin_cubrir

    return solucion


def _jugador_que_mas_cubre(jugadores, pedidos_restantes):
    """
    Encuentra el jugador que aparece en la mayor cantidad
    de pedidos restantes (regla greedy).

    Parámetros:
        jugadores: set con todos los jugadores.
        pedidos_restantes: lista de sets con los pedidos aún no cubiertos.

    Devuelve:
        string con el nombre del jugador que más pedidos cubre.
    """
    mejor_jugador = None
    mejor_cantidad = -1

    for jugador in jugadores:
        cantidad = 0
        for pedido in pedidos_restantes:
            if jugador in pedido:
                cantidad += 1

        if cantidad > mejor_cantidad:
            mejor_cantidad = cantidad
            mejor_jugador = jugador

    return mejor_jugador