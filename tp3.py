import sys
from cargador_pedidos import cargar_pedidos_de_ruta
from hitting_set_bt import hitting_set_backtracking


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 tp3.py ruta/a/listado.txt")
        return

    ruta = sys.argv[1]
    jugadores, pedidos = cargar_pedidos_de_ruta(ruta)

    solucion = hitting_set_backtracking(jugadores, pedidos)

    print(f"Cantidad mínima: {len(solucion)}")
    print(f"Jugadores: {', '.join(sorted(solucion))}")


if __name__ == "__main__":
    main()