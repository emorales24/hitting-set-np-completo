def hitting_set_greedy(jugadores, pedidos):
    """
    Logica greedy para hitting set.

    En cada paso elegimos el jugador que cubre mas pedidos que todavia
    no estaban cubiertos.

    Complejidad:
        O(n*m) por iteracion y a lo sumo n iteraciones.
        En peor caso queda O(n^2*m).

    Parametros:
        jugadores: set con todos los jugadores, o sea A
        pedidos: lista de sets, o sea los B_i

    Devuelve:
        set con los jugadores elegidos
    """
    solucion = set()
    pedidos_restantes = list(pedidos)

    while len(pedidos_restantes) > 0:
        mejor_jugador = _jugador_que_mas_cubre(jugadores, pedidos_restantes)
        solucion.add(mejor_jugador)

        # Sacamos los pedidos que ya cubre este jugador.
        pedidos_sin_cubrir = []
        for pedido in pedidos_restantes:
            if mejor_jugador not in pedido:
                pedidos_sin_cubrir.append(pedido)
        pedidos_restantes = pedidos_sin_cubrir

    return solucion


def _jugador_que_mas_cubre(jugadores, pedidos_restantes):
    """
    Busca el jugador que aparece en mas pedidos restantes.

    Devuelve:
        el nombre del jugador que mas cubre
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
