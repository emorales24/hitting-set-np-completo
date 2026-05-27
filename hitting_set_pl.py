from pulp import (
    LpMinimize,
    LpProblem,
    LpBinary,
    LpVariable,
    PULP_CBC_CMD,
    lpSum,
    value,
)


def hitting_set_pl(jugadores, pedidos):
    """
    Resuelve hitting set usando pl entera.

    Modelo:
        - x_j binaria para cada jugador j
        - x_j = 1 si elegimos al jugador, 0 si no
        - minimizar sum(x_j)
        - para cada pedido B_i, sum(x_j para j en B_i) >= 1

    Parametros:
        jugadores: set con todos los jugadores, o sea A
        pedidos: lista de sets, o sea los B_i

    Devuelve:
        set con la solucion optima
    """
    modelo = LpProblem("HittingSet_Entero", LpMinimize)

    # Var binaria por jugador
    variables = {}
    for jugador in jugadores:
        variables[jugador] = LpVariable(f"x_{jugador}", cat=LpBinary)

    # Queremos minimizar la cantidad de jugadores elegidos
    modelo += lpSum(variables[j] for j in jugadores)

    # Cada pedido tiene que quedar cubierto por al menos un jugador
    for i, pedido in enumerate(pedidos):
        modelo += lpSum(variables[j] for j in pedido) >= 1, f"pedido_{i}"

    # Resolvemos sin mostrar el log del solver
    modelo.solve(crear_solver_cbc_sin_log())

    # Pasamos las variables en 1 a un set de jugadores
    solucion = set()
    for jugador in jugadores:
        valor_variable = value(variables[jugador])
        if valor_variable is not None and valor_variable >= 0.99:
            solucion.add(jugador)

    return solucion


def crear_solver_cbc_sin_log():
    """
    Devuelve el solver CBC de PuLP sin log.
    """
    return PULP_CBC_CMD(msg=0)
