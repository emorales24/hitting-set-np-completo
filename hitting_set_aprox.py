from pulp import LpMinimize, LpProblem, LpContinuous, LpVariable, lpSum, value


def hitting_set_aprox_lp(jugadores, pedidos):
    """
    Aproximación para el Hitting Set Problem usando LP relajado
    con redondeo determinístico.

    Algoritmo:
        1. Resolver el LP relajado (variables continuas en [0, 1]).
        2. Calcular b = tamaño del pedido más grande.
        3. Redondear: x_j = 1 si x_j* >= 1/b, sino 0.

    Esta es una b-aproximación: la solución tiene a lo sumo
    b veces el tamaño de la solución óptima.

    Parámetros:
        jugadores: set con todos los jugadores (A).
        pedidos: lista de sets, donde cada set es un pedido (B_i).

    Devuelve:
        tupla (solucion, valor_b) donde:
            solucion: set con los jugadores elegidos.
            valor_b: el factor de aproximación.
    """
    modelo = LpProblem("HittingSet_Relajado", LpMinimize)

    # Variables continuas en [0, 1] (LP relajado)
    variables = {}
    for jugador in jugadores:
        variables[jugador] = LpVariable(
            f"x_{jugador}", lowBound=0, upBound=1, cat=LpContinuous
        )

    # Función objetivo: minimizar sum(x_j)
    modelo += lpSum(variables[j] for j in jugadores)

    # Restricciones: cada pedido debe sumar al menos 1
    for i, pedido in enumerate(pedidos):
        modelo += lpSum(variables[j] for j in pedido) >= 1, f"pedido_{i}"

    # Resolver
    modelo.solve(pulp_solver_sin_log())

    # Calcular b = tamaño del pedido más grande
    valor_b = _calcular_b(pedidos)

    # Redondear: si x_j* >= 1/b, entonces x_j = 1
    umbral = 1.0 / valor_b
    solucion = set()
    for jugador in jugadores:
        valor_variable = value(variables[jugador])
        if valor_variable >= umbral:
            solucion.add(jugador)

    return solucion, valor_b


def _calcular_b(pedidos):
    """
    Calcula b como el tamaño del pedido más grande.

    Parámetros:
        pedidos: lista de sets con los pedidos.

    Devuelve:
        int con el tamaño del pedido más grande.
    """
    b = 0
    for pedido in pedidos:
        if len(pedido) > b:
            b = len(pedido)
    return b


def pulp_solver_sin_log():
    """
    Devuelve un solver de PuLP configurado para no mostrar mensajes.
    """
    from pulp import PULP_CBC_CMD
    return PULP_CBC_CMD(msg=0)