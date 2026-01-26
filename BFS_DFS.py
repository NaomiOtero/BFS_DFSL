import time
from collections import deque

# =========================
# COLORES ANSI
# =========================
RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
GRAY = "\033[90m"

# =========================
# LABERINTO DEFAULT
# =========================
LABERINTO_DEFAULT = """
#####################
#S....#.........#...#
#.##.#.#.#####.#.#.##
#.#..#.#.....#.#.#.##
#.#.##.###.#.#.#.#.##
#.#......#.#.#...#.##
#.#.####.#.#.#####.##
#.#.#..#.#.#.....#.##
#...#..#...#.###.#.##
###.#######.#...#..##
#...#.....#.#.#.##.##
#.###.###.#.#.#...###
#...#...#.#...#.....#
###.#.#.#.#####.##.##
#...#.#.#.....#...###
#.###.#.###.#.###..##
#.....#.....#....G.##
#####################
""".strip("\n")


# =========================
# UTILIDADES
# =========================
def cargar_laberinto(texto):
    return [list(fila) for fila in texto.splitlines()]


def encontrar_posicion(laberinto, simbolo):
    for i, fila in enumerate(laberinto):
        for j, celda in enumerate(fila):
            if celda == simbolo:
                return (i, j)
    return None


def vecinos(laberinto, pos):
    x, y = pos
    movimientos = [(-1,0), (1,0), (0,-1), (0,1)]
    for dx, dy in movimientos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(laberinto) and 0 <= ny < len(laberinto[0]):
            if laberinto[nx][ny] != '#':
                yield (nx, ny)


# =========================
# BFS
# =========================
def bfs(laberinto):
    """
    Breadth-First Search
    Garantiza la ruta más corta
    """
    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    cola = deque([inicio])
    visitados = set([inicio])
    padre = {}
    nodos_visitados = 0

    while cola:
        actual = cola.popleft()
        nodos_visitados += 1

        if actual == meta:
            break

        for v in vecinos(laberinto, actual):
            if v not in visitados:
                visitados.add(v)
                padre[v] = actual
                cola.append(v)

    # Reconstrucción del camino
    camino = []
    actual = meta
    while actual != inicio:
        camino.append(actual)
        actual = padre.get(actual)
        if actual is None:
            return None, nodos_visitados
    camino.append(inicio)
    camino.reverse()

    return camino, nodos_visitados


# =========================
# DFS
# =========================
def dfs(laberinto):
    """
    Depth-First Search
    No garantiza la ruta más corta
    """
    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    pila = [inicio]
    visitados = set([inicio])
    padre = {}
    nodos_visitados = 0

    while pila:
        actual = pila.pop()
        nodos_visitados += 1

        if actual == meta:
            break

        for v in vecinos(laberinto, actual):
            if v not in visitados:
                visitados.add(v)
                padre[v] = actual
                pila.append(v)

    # Reconstrucción del camino
    camino = []
    actual = meta
    while actual != inicio:
        camino.append(actual)
        actual = padre.get(actual)
        if actual is None:
            return None, nodos_visitados
    camino.append(inicio)
    camino.reverse()

    return camino, nodos_visitados


# =========================
# MOSTRAR LABERINTO
# =========================
def mostrar_laberinto(laberinto, camino):
    camino_set = set(camino) if camino else set()

    for i, fila in enumerate(laberinto):
        for j, celda in enumerate(fila):
            pos = (i, j)
            if celda == 'S':
                print(YELLOW + 'S' + RESET, end='')
            elif celda == 'G':
                print(RED + 'G' + RESET, end='')
            elif pos in camino_set:
                print(GREEN + '.' + RESET, end='')
            else:
                print(GRAY + celda + RESET, end='')
        print()


# =========================
# EJECUTAR ALGORITMO
# =========================
def ejecutar(algoritmo, nombre):
    lab = cargar_laberinto(laberinto_actual)

    inicio = time.perf_counter()
    camino, nodos = algoritmo(lab)
    fin = time.perf_counter()

    print(f"\n== {nombre} ==")
    if camino:
        print(f"Longitud de la ruta: {len(camino) - 1}")
    else:
        print("No se encontró solución")

    print(f"Nodos visitados: {nodos}")
    print(f"Tiempo: {(fin - inicio) * 1000:.2f} ms\n")

    mostrar_laberinto(lab, camino)


# =========================
# MENÚ PRINCIPAL
# =========================
laberinto_actual = LABERINTO_DEFAULT

while True:
    print("\n=== Menú Principal ===")
    print("1) Resolver con BFS")
    print("2) Resolver con DFS")
    print("3) Cambiar laberinto (ruta de archivo)")
    print("4) Salir")

    opcion = input("Elige una opción: ")

    if opcion == '1':
        ejecutar(bfs, "BFS")

    elif opcion == '2':
        ejecutar(dfs, "DFS")

    elif opcion == '3':
        ruta = input("Ruta del archivo: ")
        try:
            with open(ruta, 'r') as f:
                laberinto_actual = f.read().strip()
            print("Laberinto cargado correctamente.")
        except:
            print("Error al leer el archivo.")

    elif opcion == '4':
        print("Saliendo...")
        break

    else:
        print("Opción inválida.")
