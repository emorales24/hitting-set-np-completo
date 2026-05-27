def hitting_set_backtracking(jugadores, pedidos):
    """
    Resuelve hitting set exacto con bt.

    Busca el C mas chico posible tal que toque todos los pedidos.

    Parametros:
        jugadores: set con todos los jugadores, o sea A
        pedidos: lista de sets, o sea los B_i

    Devuelve:
        set con la solucion optima C
    """
    mejor_solucion = set(jugadores)  # peor caso: todos los jugadores
    solucion_parcial = set()

    mejor_solucion = _backtrack(pedidos, solucion_parcial, mejor_solucion)

    return mejor_solucion


def _backtrack(pedidos_restantes, solucion_parcial, mejor_solucion):
    """
    Paso recursivo del bt.

    Agarra un pedido que falta cubrir y prueba elegir cada jugador de ese pedido.

    Parametros:
        pedidos_restantes: pedidos que todavia no estan cubiertos
        solucion_parcial: jugadores elegidos hasta ahora
        mejor_solucion: mejor solucion encontrada hasta ahora

    Devuelve:
        la mejor solucion encontrada hasta este punto
    """
    # caso base: si no quedan pedidos, ya cubrimos todo
    if len(pedidos_restantes) == 0:
        if len(solucion_parcial) < len(mejor_solucion):
            mejor_solucion = set(solucion_parcial)
        return mejor_solucion

    # caso base: si ya no podemos mejorar la mejor solucion, cortamos esta rama
    if len(solucion_parcial) >= len(mejor_solucion) - 1:
        return mejor_solucion

    # Elegimos primero el pedido con menos opciones
    pedido_elegido = _pedido_mas_restrictivo(pedidos_restantes)

    # Probamos cada jugador posible para cubrir ese pedido
    for jugador in pedido_elegido:
        solucion_parcial.add(jugador)

        # Sacamos los pedidos que ya quedan cubiertos por este jugador.
        pedidos_sin_cubrir = _filtrar_pedidos_cubiertos(pedidos_restantes, jugador)

        mejor_solucion = _backtrack(
            pedidos_sin_cubrir, solucion_parcial, mejor_solucion
        )

        solucion_parcial.remove(jugador)

    return mejor_solucion


def _pedido_mas_restrictivo(pedidos):
    """
    Devuelve el pedido con menos jugadores.

    La idea es ramificar primero por el pedido que tiene menos opciones.

    Devuelve:
        set con el pedido mas chico
    """
    pedido_minimo = pedidos[0]

    for pedido in pedidos:
        if len(pedido) < len(pedido_minimo):
            pedido_minimo = pedido

    return pedido_minimo


def _filtrar_pedidos_cubiertos(pedidos, jugador):
    """
    Devuelve los pedidos que el jugador elegido no cubre.

    Si el jugador esta en un pedido, ese pedido ya no hace falta seguirlo.

    Devuelve:
        lista de pedidos que siguen sin cubrir
    """
    pedidos_sin_cubrir = []

    for pedido in pedidos:
        if jugador not in pedido:
            pedidos_sin_cubrir.append(pedido)

    return pedidos_sin_cubrir
