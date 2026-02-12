import time
import heapq
from collections import deque
import math

RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
BLUE = "\033[94m"

LABERINTO_DEFAULT = """
###################
#S..,,..........#G#
#.###.###########.#
#...#.......,,,,..#
#.#.#.#########.#.#
#.#.#.....~~~~~.#.#
#.#.###########.#.#
#.#.............#.#
#.###############.#
#.................#
###################
""".strip("\n")


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


def costo_celda(laberinto, pos):
    x, y = pos
    simbolo = laberinto[x][y]

    if simbolo == 'S' or simbolo == 'G':
        return 0
    elif simbolo == '.':
        return 1
    elif simbolo == ',':
        return 5
    elif simbolo == '~':
        return 10
    else:
        return float('inf')
    


def costo_camino(laberinto, camino): 
    if not camino:
        return float('inf')

    total = 0
    for pos in camino:
        total += costo_celda(laberinto, pos)
    return total


def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def heuristica_euclidiana(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def ucs(laberinto):
    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    cola = []
    heapq.heappush(cola, (0, inicio))

    costos = {inicio: 0}
    padre = {}
    visitados = set()
    nodos_visitados = 0

    while cola:
        costo_actual, actual = heapq.heappop(cola)

        if actual in visitados:
            continue

        visitados.add(actual)
        nodos_visitados += 1

        if actual == meta:
            break

        for v in vecinos(laberinto, actual):
            nuevo_costo = costo_actual + costo_celda(laberinto, v)

            if v not in costos or nuevo_costo < costos[v]:
                costos[v] = nuevo_costo
                padre[v] = actual
                heapq.heappush(cola, (nuevo_costo, v))

    camino = []
    actual = meta
    while actual != inicio:
        camino.append(actual)
        actual = padre.get(actual)
        if actual is None:
            return None, nodos_visitados, float('inf')
    camino.append(inicio)
    camino.reverse()

    return camino, nodos_visitados, costos[meta]


def astar(laberinto, heuristica):
    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    abiertos = [] #es el arreglo de los nodos sin vis
    heapq.heappush(abiertos, (0, inicio)) #cola de prioridad 

    g_costos = {inicio: 0}
    padre = {}
    cerrados = set() # no repetir nodos 
    nodos_visitados = 0

    while abiertos:
        _, actual = heapq.heappop(abiertos)

        if actual in cerrados:
            continue

        cerrados.add(actual)
        nodos_visitados += 1

        if actual == meta:
            break

        for v in vecinos(laberinto, actual):
            nuevo_g = g_costos[actual] + costo_celda(laberinto, v)

            if v in cerrados and nuevo_g >= g_costos.get(v, float('inf')): 
                continue

            if nuevo_g < g_costos.get(v, float('inf')):
                padre[v] = actual
                g_costos[v] = nuevo_g
                f = nuevo_g + heuristica(v, meta) #g es costo acumulado v donde nos encontramos y y la direccion de la meta 
                heapq.heappush(abiertos, (f, v)) #ordenar por menor 

    camino = []
    actual = meta
    while actual != inicio:
        camino.append(actual)
        actual = padre.get(actual)
        if actual is None:
            return None, nodos_visitados, float('inf')
    camino.append(inicio)
    camino.reverse()

    return camino, nodos_visitados, g_costos[meta]


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
                print(GREEN + celda + RESET, end='')
            else:
                print(GRAY + celda + RESET, end='')
        print()


def ejecutar_ucs():
    lab = cargar_laberinto(laberinto_actual)

    inicio = time.perf_counter()
    camino, nodos, costo = ucs(lab)
    fin = time.perf_counter()

    print("\n== UCS ==")
    if camino:
        print(f"Longitud de la ruta: {len(camino) - 1}")
        print(f"Costo total: {costo}")
    else:
        print("No se encontró solución")

    print(f"Nodos visitados: {nodos}")
    print(f"Tiempo: {(fin - inicio) * 1000:.2f} ms\n")

    mostrar_laberinto(lab, camino)


def ejecutar_astar(heuristica, nombre):
    lab = cargar_laberinto(laberinto_actual)

    inicio = time.perf_counter()
    camino, nodos, costo = astar(lab, heuristica)
    fin = time.perf_counter()

    print(f"\n== A* ({nombre}) ==")
    if camino:
        print(f"Longitud de la ruta: {len(camino) - 1}")
        print(f"Costo total: {costo}")
    else:
        print("No se encontró solución")

    print(f"Nodos visitados: {nodos}")
    print(f"Tiempo: {(fin - inicio) * 1000:.2f} ms\n")

    mostrar_laberinto(lab, camino)


laberinto_actual = LABERINTO_DEFAULT

ejecutando = True
while ejecutando:
    print("\n=== Menú Principal ===")
    print("1) Resolver con UCS")
    print("2) A* con heurística Manhattan")
    print("3) A* con heurística Euclidiana")
    print("4) Cambiar laberinto (.txt)")
    print("5) Salir")

    opcion = input("Elige una opción: ")

    if opcion == '1':
        ejecutar_ucs()

    elif opcion == '2':
        ejecutar_astar(heuristica_manhattan, "Manhattan")

    elif opcion == '3':
        ejecutar_astar(heuristica_euclidiana, "Euclidiana")
    
    elif opcion =='4':
        ruta = input("Ruta del archivo: ")
        try:
             with open(ruta, 'r') as f:
                 laberinto_actual = f.read().strip()
             print("Laberinto cargado correctamente.")
        except:
            print("Error al leer el archivo.")

    elif opcion == '5':
        print("Saliendo...")
        ejecutando = False

    else:
        print("Opción inválida.")
