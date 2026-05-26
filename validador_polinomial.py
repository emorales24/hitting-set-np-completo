"""
Una solucion esta dada por un subconjunto C contenido en A.

Dicha solucion es valida si C contiene al menos un elemento
en comun con cada uno de los B_1, B_2, ..., B_m.
"""


def validador_polinomial(solucion, jugadores, pedidos):
    """
    solucion = C
    jugadores = A
    pedidos = [B_1, B_2, ..., B_m]
    """

    if not solucion.issubset(jugadores):
        return False

    for pedido in pedidos:
        if solucion.isdisjoint(pedido):
            return False

    return True


# Complejidad:
# Sea m la cantidad de pedidos y k = |C| la cantidad de jugadores
# en la solucion.
#
# Verificar que C esta contenido en A cuesta O(k), ya que issubset
# verifica, para cada jugador de C, que este pertenezca a A.
# Como A es un set, cada consulta de pertenencia cuesta O(1) en promedio.
#
# Para cada B_i se verifica que C interseque en al menos un jugador.
# En el peor caso, para cada uno de los m pedidos se revisan los k
# jugadores de C. Como cada B_i es un un set, consultar si un jugador
# pertenece a B_i cuesta O(1) en promedio. Entonces, cuesta O(m*k).
#
# La complejidad total es O(k + m*k), que se simplifica a O(m*k).
# Como k <= n, tambien queda acotada por O(m*n).
#
# Por lo tanto, el validador corre en tiempo polinomial.
