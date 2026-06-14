"""
Validadores polinomiales para Hitting Set.

Una solucion esta dada por un subconjunto C contenido en A.

La condicion base es que C tenga al menos un jugador en comun
con cada pedido B_i.
"""


def validar_cobertura(solucion, jugadores, pedidos):
    """
    Valida que una solucion C cubra todos los pedidos.

    solucion = C
    jugadores = A
    pedidos = [B_1, B_2, ..., B_m]

    Devuelve True si:
    - C esta dentro de A
    - para todo B_i, C tiene al menos un jugador en comun con B_i
    """
    if not solucion.issubset(jugadores):
        return False

    for pedido in pedidos:
        if solucion.isdisjoint(pedido):
            return False

    return True


def validar_decision(solucion, jugadores, pedidos, k):
    """
    Valida un certificado para la version de decision.

    La version de decision pregunta si existe un C tal que:
    - C esta dentro de A
    - |C| <= k
    - para todo B_i, C tiene al menos un jugador en comun con B_i
    """
    if len(solucion) > k:
        return False

    return validar_cobertura(solucion, jugadores, pedidos)


def validar_optimo_conocido(solucion, jugadores, pedidos, cantidad_minima):
    """
    Valida una solucion cuando ya sabemos cuanto deberia medir el optimo.
    Sirve para comparar contra los tests de la catedra.
    """
    if len(solucion) != cantidad_minima:
        return False

    return validar_cobertura(solucion, jugadores, pedidos)


# Complejidad de validar_cobertura:
# Sea m la cantidad de pedidos y c = |C| la cantidad de jugadores de la
# solucion que estamos validando.
#
# Verificar que C esta contenido en A cuesta O(c), ya que issubset
# verifica, para cada jugador de C, que este pertenezca a A.
# Como A es un set, cada consulta de pertenencia cuesta O(1) en promedio.
#
# Para cada B_i se verifica que C tenga al menos un jugador en comun.
# En el peor caso, para cada uno de los m pedidos se revisan los c
# jugadores de C. Como cada B_i es un set, consultar si un jugador
# pertenece a B_i cuesta O(1) en promedio. Entonces esta parte cuesta O(m*c).
#
# La complejidad total es O(c + m*c), que se simplifica a O(m*c).
# Como c <= n, tambien queda acotada por O(m*n).
#
# Complejidad de validar_decision:
# Agrega el chequeo |C| <= k, que cuesta O(1). Entonces tambien
# cuesta O(m*c), acotado por O(m*k) para certificados validos y por O(m*n).
#
# Complejidad de validar_optimo_conocido:
# Agrega el chequeo |C| == cantidad_minima, que cuesta O(1). Entonces
# tambien cuesta O(m*c), acotado por O(m*n).
#
# En todos los casos, los validadores corren en tiempo polinomial.
