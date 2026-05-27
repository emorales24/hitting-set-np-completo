import random
import os

NOMBRES_JUGADORES = [
    "Messi",
    "Dibu",
    "Cuti Romero",
    "De Paul",
    "Mac Allister",
    "Alvarez",
    "Molina",
    "Tagliafico",
    "Otamendi",
    "Paredes",
    "Di Maria",
    "Dybala",
    "Lautaro",
    "Enzo Fernandez",
    "Gonzalo Montiel",
    "Nico Gonzalez",
    "Licha Martinez",
    "Pezzella",
    "Guido Rodriguez",
    "Exequiel Palacios",
    "Almada",
    "Garnacho",
    "Simeone",
    "Beltran",
    "Soule",
    "Carboni",
    "Buonanotte",
    "Barco",
    "Nico Paz",
    "Castellanos",
    "Senesi",
    "Medina",
    "Palacios",
    "Fernandez",
    "Ascacibar",
    "Echeverri",
    "Colidio",
    "Langoni",
    "Zeballos",
    "Romero",
    "Armani",
    "Musso",
    "Rulli",
    "Acuna",
    "Foyth",
    "Cristian Romero",
    "Lisandro Lopez",
    "Correa",
    "Pereyra",
    "Lanzini",
    "Papu Gomez",
    "Lo Celso",
    "Ocampos",
    "Aguero",
    "Higuain",
    "Icardi",
    "Riquelme",
    "Palermo",
    "Crespo",
    "Batistuta",
    "Gallardo",
    "Aimar",
    "Saviola",
    "Tevez",
    "Mascherano",
    "Zanetti",
    "Samuel",
    "Heinze",
    "Sorin",
    "Cambiasso",
    "Veron",
    "Ortega",
    "Redondo",
    "Simeone Sr",
    "Caniggia",
    "Valdano",
    "Burruchaga",
    "Maradona",
    "Kempes",
    "Passarella",
    "Fillol",
    "Luque",
    "Bertoni",
    "Ardiles",
    "Tarantini",
    "Houseman",
    "Babington",
    "Brindisi",
    "Yazalde",
    "Perfumo",
    "Rattin",
    "Onega",
    "Mas",
    "Arco",
    "Sivori",
    "Labruna",
    "Pedernera",
    "Loustau",
    "Di Stefano",
    "Moreno",
    "Sastre",
]


def _generar_jugadores(cantidad):
    """
    Genera nombres de jugadores.
    Si no alcanzan con los nombres reales, agrega "Jugador_{indice}".
    """
    if cantidad <= len(NOMBRES_JUGADORES):
        return NOMBRES_JUGADORES[:cantidad]

    jugadores = list(NOMBRES_JUGADORES)
    indice = len(NOMBRES_JUGADORES)
    while len(jugadores) < cantidad:
        jugadores.append(f"Jugador_{indice}")
        indice += 1

    return jugadores


def generar_instancia(n, m, min_tam_pedido, max_tam_pedido, semilla=None):
    """
    Genera una instancia aleatoria de hitting set.

    Parametros:
        n: cantidad de jugadores
        m: cantidad de pedidos
        min_tam_pedido: tamanio minimo de cada pedido
        max_tam_pedido: tamanio maximo de cada pedido
        semilla: para poder repetir el mismo set

    Devuelve:
        jugadores y pedidos generados
    """
    if semilla is not None:
        random.seed(semilla)

    jugadores = _generar_jugadores(n)
    pedidos = []

    for _ in range(m):
        tam = random.randint(min_tam_pedido, max_tam_pedido)
        tam = min(tam, n)
        pedido = set(random.sample(jugadores, tam))
        pedidos.append(pedido)

    return jugadores, pedidos


def generar_caso_facil(n, semilla=None):
    """
    Genera un caso facil.
    Hay un jugador que aparece en muchos pedidos, entonces
    el optimo tiende a ser chico.
    """
    if semilla is not None:
        random.seed(semilla)

    jugadores = _generar_jugadores(n)
    m = n * 2
    pedidos = []
    estrella = jugadores[0]

    for _ in range(m):
        tam = random.randint(2, max(3, n // 3))
        pedido = set(random.sample(jugadores, tam))
        if random.random() < 0.7:
            pedido.add(estrella)
        pedidos.append(pedido)

    return jugadores, pedidos


def generar_caso_dificil(n, semilla=None):
    """
    Genera un caso mas dificil para el bt.
    Los pedidos son chicos y se pisan poco, entonces hay mas ramas.
    """
    if semilla is not None:
        random.seed(semilla)

    jugadores = _generar_jugadores(n)
    m = n * 3
    pedidos = []

    for _ in range(m):
        tam = random.randint(2, 3)
        tam = min(tam, n)
        pedido = set(random.sample(jugadores, tam))
        pedidos.append(pedido)

    return jugadores, pedidos


def generar_caso_todos(n, semilla=None):
    """
    Genera un caso donde todos los jugadores son necesarios.
    Cada pedido tiene un solo jugador.
    """
    if semilla is not None:
        random.seed(semilla)

    jugadores = _generar_jugadores(n)
    pedidos = []

    for jugador in jugadores:
        pedidos.append({jugador})

    return jugadores, pedidos


def guardar_instancia(ruta, jugadores, pedidos):
    """
    Guarda una instancia con el formato de la catedra:
    un pedido por linea y jugadores separados por coma.
    """
    directorio = os.path.dirname(ruta)
    if directorio and not os.path.exists(directorio):
        os.makedirs(directorio)

    with open(ruta, "w", encoding="utf-8") as archivo:
        for pedido in pedidos:
            linea = ", ".join(sorted(pedido))
            archivo.write(linea + "\n")


def generar_sets_completos(directorio_salida, semilla=42):
    """
    Genera sets propios (los usados para medir).

    Devuelve:
        lista con (nombre_archivo, n, m, tipo)
    """
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)

    sets_generados = []

    # Sets aleatorios de distintos tamanios.
    tamanos = [10, 15, 20, 30, 40, 50, 75, 100]
    for n in tamanos:
        m = n * 2
        min_tam = 2
        max_tam = max(3, n // 4)
        nombre = f"aleatorio_{n}.txt"
        ruta = os.path.join(directorio_salida, nombre)
        jugadores, pedidos = generar_instancia(
            n, m, min_tam, max_tam, semilla=semilla + n
        )
        guardar_instancia(ruta, jugadores, pedidos)
        sets_generados.append((nombre, n, m, "aleatorio"))

    # Sets faciles.
    for n in [20, 50, 100]:
        nombre = f"facil_{n}.txt"
        ruta = os.path.join(directorio_salida, nombre)
        jugadores, pedidos = generar_caso_facil(n, semilla=semilla + n + 1000)
        guardar_instancia(ruta, jugadores, pedidos)
        sets_generados.append((nombre, n, len(pedidos), "facil"))

    # Sets dificiles.
    for n in [10, 15, 20, 25, 30]:
        nombre = f"dificil_{n}.txt"
        ruta = os.path.join(directorio_salida, nombre)
        jugadores, pedidos = generar_caso_dificil(n, semilla=semilla + n + 2000)
        guardar_instancia(ruta, jugadores, pedidos)
        sets_generados.append((nombre, n, len(pedidos), "dificil"))

    # Sets donde todos son necesarios.
    for n in [5, 10, 15]:
        nombre = f"todos_{n}.txt"
        ruta = os.path.join(directorio_salida, nombre)
        jugadores, pedidos = generar_caso_todos(n, semilla=semilla + n + 3000)
        guardar_instancia(ruta, jugadores, pedidos)
        sets_generados.append((nombre, n, len(pedidos), "todos"))

    return sets_generados


if __name__ == "__main__":
    sets = generar_sets_completos("archivos-test-propios")
    print(f"Se generaron {len(sets)} sets de datos:")
    for nombre, n, m, tipo in sets:
        print(f"  {nombre}: n={n}, m={m}, tipo={tipo}")
