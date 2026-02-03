import time
import heapq #Para ucs
from collections import deque


RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
GRAY = "\033[90m"


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

#struct para definir los pesos de los simbolos en los laberintos practica2
COSTOS = {
    '.': 1,
    ',': 5,
    '~': 10
}




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


#nueva funcion para el calculo del costo de la celda practica2
def costo_celda(laberinto, pos):
    x, y = pos
    simbolo = laberinto[x][y]

    if simbolo == 'S' or simbolo == 'G':
        return 0  # inicio y meta no cuestan

    return COSTOS.get(simbolo, float('inf'))

#nueva funcion para calcular el costo de los caminos con peso practica2
def costo_camino(laberinto, camino):
    if not camino:
        return float('inf')
    return sum(costo_celda(laberinto, pos) for pos in camino)




def bfs(laberinto):
    
    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    cola = deque([inicio])
    visitados = set([inicio])
    padre = {}
    nodos_visitados = 0

    while cola:         #la cola continua mientras haya nodos en la cola, si la cola esta vacia, no hay mas caminos posibles
        actual = cola.popleft()
        nodos_visitados = nodos_visitados + 1 #afectada

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



def dfs(laberinto):
  
    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    pila = [inicio]
    visitados = set([inicio])
    padre = {}
    nodos_visitados = 0

    while pila:                                                                 #se ejecuta mientras haya nodos en la pila, si la pila esta vacia no hay mas caminos
        actual = pila.pop()
        nodos_visitados = nodos_visitados + 1 #afectada

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


#algoritmo de costos uniformes
def ucs(laberinto):
    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    cola = []
    heapq.heappush(cola, (0, inicio))

    costos = {inicio: 0}
    padre = {}
    visitados = set()
    nodos_visitados = 0

    while len(cola) > 0:
        costo_actual, actual = heapq.heappop(cola)

        if actual in visitados:
            continue

        visitados.add(actual)
        nodos_visitados = nodos_visitados + 1

        if actual == meta:
            break

        for v in vecinos(laberinto, actual):
            nuevo_costo = costo_actual + costo_celda(laberinto, v)

            if v not in costos or nuevo_costo < costos[v]:
                costos[v] = nuevo_costo
                padre[v] = actual
                heapq.heappush(cola, (nuevo_costo, v))


    #reconstruccion del camino
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




def mostrar_laberinto(laberinto, camino):
    camino_set = set(camino) if camino else set()

    for i, fila in enumerate(laberinto):
        for j, celda in enumerate(fila):
            pos = (i, j)
            if celda == 'S':
                print(YELLOW + 'S' + RESET, end='')
            elif celda == 'G':
                print(RED + 'G' + RESET, end='')
                #se cambio '.' a celda para que los 3 algoritmos puedan imprimir todos los simbolos
            elif pos in camino_set:
                print(GREEN + celda + RESET, end='') 
            else:
                print(GRAY + celda + RESET, end='')
        print()


def ejecutar(algoritmo, nombre):
    lab = cargar_laberinto(laberinto_actual)

    inicio = time.perf_counter()
    
    #actualizacion en ejecutar para poder usas ucs
    if nombre == "UCS":
        camino, nodos, costo = algoritmo(lab)
    else:
        camino, nodos = algoritmo(lab)
        costo = costo_camino(lab, camino)

    fin = time.perf_counter()

    print(f"\n== {nombre} ==")
    if camino:
        print(f"Longitud de la ruta: {len(camino) - 1}")
        print(f"Costo total: {costo}") #mostrar costo del camino
    else:
        print("No se encontró solución")

    print(f"Nodos visitados: {nodos}")
    print(f"Tiempo: {(fin - inicio) * 1000:.2f} ms\n")

    mostrar_laberinto(lab, camino)



laberinto_actual = LABERINTO_DEFAULT

while True:
    print("\n=== Menú Principal ===")
    print("1) Resolver con BFS")
    print("2) Resolver con DFS")
    print("3) Resolver con UCS")
    print("4) Cambiar laberinto (ruta de archivo)")
    print("5) Salir")

    opcion = input("Elige una opción: ")

    if opcion == '1':
        ejecutar(bfs, "BFS")

    elif opcion == '2':
        ejecutar(dfs, "DFS")
        
    elif opcion == '3':
        ejecutar(ucs, "UCS")

    elif opcion == '4':
        ruta = input("Ruta del archivo: ")
        try:
            with open(ruta, 'r') as f:
                laberinto_actual = f.read().strip()
            print("Laberinto cargado correctamente.")
        except:
            print("Error al leer el archivo.")

    elif opcion == '5':
        print("Saliendo...")
        break

    else:
        print("Opción inválida.")
