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
    return [list(fila) for fila in texto.splitlines()] # Convierte el texto del laberinto en una lista de listas


def encontrar_posicion(laberinto, simbolo): # Encuentra la posición de un símbolo en el laberinto
    for i, fila in enumerate(laberinto): # Recorre cada fila del laberinto
        for j, celda in enumerate(fila): # Recorre cada celda de la fila
            if celda == simbolo: # Si la celda coincide con el símbolo buscado
                return (i, j) #devuelve la posicion 
    return None


def vecinos(laberinto, pos):
    x, y = pos #posicion actual
    movimientos = [(-1,0), (1,0), (0,-1), (0,1)] #solo podemos mover arriba, abajo, izquierda, derecha
    for dx, dy in movimientos: #recorre los movimientos posibles
        nx, ny = x + dx, y + dy #nueva posicion
        if 0 <= nx < len(laberinto) and 0 <= ny < len(laberinto[0]): #verifica que la nueva posicion este dentro de los limites del laberinto
            if laberinto[nx][ny] != '#': #verifica que la  posicion no sea una pared #
                yield (nx, ny) #devuelve la nueva posicion


# =========================
# BFS
# =========================
def bfs(laberinto):
    """
    Breadth-First Search
    Garantiza la ruta más corta
    """
    inicio = encontrar_posicion(laberinto, 'S') #posicion de inicio
    meta = encontrar_posicion(laberinto, 'G') #posicion de meta

    cola = deque([inicio]) #cola para BFS
    visitados = set([inicio]) #conjunto de nodos visitados
    padre = {} #diccionario para reconstruir el camino
    nodos_visitados = 0 #contador de nodos visitados

    while cola:
        actual = cola.popleft() #saca el primer elemento de la cola
        nodos_visitados += 1 #incrementa el contador de nodos visitados

        if actual == meta: #si se llega a la meta
            break 

        for v in vecinos(laberinto, actual): #|recorre los vecinos del nodo actual
            if v not in visitados:#si el vecino no ha sido visitado
                visitados.add(v) #lo marca como visitado
                padre[v] = actual #registra el padre del nodo vecino
                cola.append(v) #lo añade a la cola

    # Reconstrucción del camino
    camino = []
    actual = meta #comienza desde la meta
    while actual != inicio: #mientras no se llegue al inicio
        camino.append(actual) #añade el nodo actual al camino
        actual = padre.get(actual) #obtiene el padre del nodo actual
        if actual is None: #si no hay padre, no se encontró camino
            return None, nodos_visitados #devuelve None y el numero de nodos visitados
    camino.append(inicio) #añade el nodo de inicio al camino
    camino.reverse() #invierte el camino para que vaya del inicio a la meta

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
        actual = pila.pop() #saca el ultimo elemento de la pila
        nodos_visitados += 1 #incrementa el contador de nodos visitados

        if actual == meta: #si se llega a la meta
            break

        for v in vecinos(laberinto, actual): #||recorre los vecinos del nodo actual
            if v not in visitados: #si el vecino no ha sido visitado
                visitados.add(v) #lo marca como visitado
                padre[v] = actual #registra el padre del nodo vecino
                pila.append(v) #lo añade a la pila
    # Reconstrucción del camino
    camino = []
    actual = meta
    while actual != inicio:
        camino.append(actual) #añade el nodo actual al camino
        actual = padre.get(actual) #obtiene el padre del nodo actual
        if actual is None:
            return None, nodos_visitados #devuelve None y el numero de nodos visitados
    camino.append(inicio)
    camino.reverse()

    return camino, nodos_visitados


# =========================
# MOSTRAR LABERINTO
# =========================
def mostrar_laberinto(laberinto, camino):
    camino_set = set(camino) if camino else set()
 #COLORE S Y G PARA DESTACARLOS 
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
def ejecutar(algoritmo, nombre): #ejecuta el algoritmo seleccionado
    lab = cargar_laberinto(laberinto_actual)

    inicio = time.perf_counter()
    camino, nodos = algoritmo(lab) #ejecuta el algoritmo seleccionado
    fin = time.perf_counter()

    print(f"\n== {nombre} ==")
    if camino:
        print(f"Longitud de la ruta: {len(camino) - 1}") #resta 1 para no contar el nodo inicial
    else:
        print("No se encontró solución")

    print(f"Nodos visitados: {nodos}")
    print(f"Tiempo: {(fin - inicio) * 1000:.2f} ms\n") #tiempo en milisegundos

    mostrar_laberinto(lab, camino) #muestra el laberinto con el camino encontrado


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
            with open(ruta, 'r') as f: #abre el archivo en modo lectura
                laberinto_actual = f.read().strip()
            print("Laberinto cargado correctamente.")
        except:
            print("Error al leer el archivo.")

    elif opcion == '4':
        print("Saliendo...")
        break

    else:
        print("Opción inválida.")
