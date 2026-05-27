from pulp import LpMinimize, LpProblem, LpContinuous, LpVariable, lpSum, value


def hitting_set_aprox_lp(jugadores, pedidos):
    """
    Aproximacion por LP relajado y redondeo.

    Algoritmo:
        1. resolvemos el LP relajado, o sea con cualquier valor entre [0, 1]
        2. calculamos b como el tamanio del pedido mas grande
        3. elegimos j si x_j >= 1/b

    La cota de aproximacion es b.

    Parametros:
        jugadores: set con todos los jugadores, o sea A
        pedidos: lista de sets, o sea los B_i

    Devuelve:
        (solucion, valor_b)
    """
    modelo = LpProblem("HittingSet_Relajado", LpMinimize)

    # Variables continuas en [0, 1].
    variables = {}
    for jugador in jugadores:
        variables[jugador] = LpVariable(
            f"x_{jugador}", lowBound=0, upBound=1, cat=LpContinuous
        )

    # Misma funcion objetivo que el modelo entero.
    modelo += lpSum(variables[j] for j in jugadores)

    # Cada pedido tiene que sumar al menos 1.
    for i, pedido in enumerate(pedidos):
        modelo += lpSum(variables[j] for j in pedido) >= 1, f"pedido_{i}"

    # Resolvemos el LP relajado.
    modelo.solve(pulp_solver_sin_log())

    # b es el tamanio del pedido mas grande.
    valor_b = _calcular_b(pedidos)

    # Si x_j >= 1/b, lo agregamos a la solucion.
    umbral = 1.0 / valor_b
    solucion = set()
    for jugador in jugadores:
        valor_variable = value(variables[jugador])
        if valor_variable >= umbral:
            solucion.add(jugador)

    return solucion, valor_b


def _calcular_b(pedidos):
    """
    Calcula b como el tamanio del pedido mas grande.
    """
    b = 0
    for pedido in pedidos:
        if len(pedido) > b:
            b = len(pedido)
    return b


def pulp_solver_sin_log():
    """
    Devuelve el solver CBC de PuLP sin log.
    """
    from pulp import PULP_CBC_CMD

    return PULP_CBC_CMD(msg=0)
