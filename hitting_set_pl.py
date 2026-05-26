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
    Resuelve el Hitting Set Problem de forma exacta usando
    programación lineal entera (ILP).

    Modelo:
        - Variable binaria x_j para cada jugador j en A.
          x_j = 1 si el jugador j es elegido, 0 si no.
        - Minimizar: sum(x_j) para todo j en A.
        - Restricciones: para cada pedido B_i,
          sum(x_j para j en B_i) >= 1.
          (cada pedido debe tener al menos un jugador elegido)

    Parámetros:
        jugadores: set con todos los jugadores (A).
        pedidos: lista de sets, donde cada set es un pedido (B_i).

    Devuelve:
        set con los jugadores de la solución óptima.
    """
    modelo = LpProblem("HittingSet_Entero", LpMinimize)

    # Variables de decisión: x_j binaria por cada jugador
    variables = {}
    for jugador in jugadores:
        variables[jugador] = LpVariable(f"x_{jugador}", cat=LpBinary)

    # Función objetivo: minimizar la cantidad de jugadores elegidos
    modelo += lpSum(variables[j] for j in jugadores)

    # Restricciones: cada pedido debe tener al menos un jugador
    for i, pedido in enumerate(pedidos):
        modelo += lpSum(variables[j] for j in pedido) >= 1, f"pedido_{i}"

    # Resolver sin mostrar output del solver
    modelo.solve(crear_solver_cbc_sin_log())

    # Extraer la solución
    solucion = set()
    for jugador in jugadores:
        valor_variable = value(variables[jugador])
        if valor_variable is not None and valor_variable >= 0.99:
            solucion.add(jugador)

    return solucion


def crear_solver_cbc_sin_log():
    """
    Devuelve el solver CBC de PuLP configurado para no mostrar mensajes.
    """
    return PULP_CBC_CMD(msg=0)
