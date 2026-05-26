def hitting_set_backtracking(jugadores, pedidos):
    """
    Resuelve el Hitting Set Problem de forma exacta usando backtracking.

    Dado un conjunto de jugadores (A) y una lista de pedidos (B_1, ..., B_m),
    encuentra el subconjunto C de A de menor tamaño tal que C intersecte
    a todos los pedidos.

    Parámetros:
        jugadores: set con todos los jugadores (A).
        pedidos: lista de sets, donde cada set es un pedido (B_i).

    Devuelve:
        set con los jugadores de la solución óptima (C).
    """
    mejor_solucion = set(jugadores)  # peor caso: todos los jugadores
    solucion_parcial = set()

    mejor_solucion = _backtrack(pedidos, solucion_parcial, mejor_solucion)

    return mejor_solucion


def _backtrack(pedidos_restantes, solucion_parcial, mejor_solucion):
    """
    Función recursiva del backtracking.

    En cada llamada, busca un pedido no cubierto y ramifica eligiendo
    cada jugador de ese pedido como candidato.

    Parámetros:
        pedidos_restantes: lista de sets con los pedidos aún no cubiertos.
        solucion_parcial: set con los jugadores elegidos hasta ahora.
        mejor_solucion: set con la mejor solución encontrada hasta ahora.

    Devuelve:
        set con la mejor solución encontrada.
    """
    # Caso base: si no quedan pedidos, todos fueron cubiertos
    if len(pedidos_restantes) == 0:
        if len(solucion_parcial) < len(mejor_solucion):
            mejor_solucion = set(solucion_parcial)
        return mejor_solucion

    # Poda: si la solución parcial ya es tan grande como la mejor, cortamos
    if len(solucion_parcial) >= len(mejor_solucion) - 1:
        return mejor_solucion

    # MRV: elegimos el pedido no cubierto con menos jugadores
    pedido_elegido = _pedido_mas_restrictivo(pedidos_restantes)

    # Ramificamos: probamos con cada jugador del pedido elegido
    for jugador in pedido_elegido:
        solucion_parcial.add(jugador)

        # Propagación: filtramos los pedidos que este jugador cubre
        pedidos_sin_cubrir = _filtrar_pedidos_cubiertos(pedidos_restantes, jugador)

        mejor_solucion = _backtrack(pedidos_sin_cubrir, solucion_parcial, mejor_solucion)

        solucion_parcial.remove(jugador)

    return mejor_solucion


def _pedido_mas_restrictivo(pedidos):
    """
    Devuelve el pedido con menor cantidad de jugadores (heurística MRV).

    Al elegir el pedido más restrictivo primero, se generan menos ramas
    en el árbol de backtracking.

    Parámetros:
        pedidos: lista de sets con los pedidos restantes.

    Devuelve:
        set con el pedido que tiene menos jugadores.
    """
    pedido_minimo = pedidos[0]

    for pedido in pedidos:
        if len(pedido) < len(pedido_minimo):
            pedido_minimo = pedido

    return pedido_minimo


def _filtrar_pedidos_cubiertos(pedidos, jugador):
    """
    Devuelve los pedidos que el jugador elegido NO cubre.

    Un pedido queda cubierto si el jugador pertenece a él,
    por lo que no necesita ser procesado en la recursión.

    Parámetros:
        pedidos: lista de sets con los pedidos actuales.
        jugador: string con el nombre del jugador elegido.

    Devuelve:
        lista de sets con los pedidos que aún no están cubiertos.
    """
    pedidos_sin_cubrir = []

    for pedido in pedidos:
        if jugador not in pedido:
            pedidos_sin_cubrir.append(pedido)

    return pedidos_sin_cubrir