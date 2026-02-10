import time
import heapq #Para ucs y A*
from collections import deque
import math #importamos la libreria de math para las heuristicas


RESET = "\033[0m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
GRAY = "\033[90m"
BLUE = "\033[94m"   # nuevo color para marcar los nodos abiertos en la impresion del algoritmo A*



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


#nueva funcion para el calculo del costo de la celda practica2
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


#nueva funcion para calcular el costo de los caminos con peso practica2
def costo_camino(laberinto, camino):
    if len(camino) == 0:
        return float('inf')

    else:
        total = 0
    for pos in camino:
        total = total + costo_celda(laberinto, pos)

    return total

#funciones con las formulas de las heuristicas
def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def heuristica_euclidiana(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)


def bfs(laberinto):
    
    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    cola = deque([inicio])
    visitados = set([inicio])
    padre = {}
    nodos_visitados = 0

    while cola:                                                      #la cola continua mientras haya nodos en la cola, si la cola esta vacia, no hay mas caminos posibles
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


#Algoritmo de A*

def astar(laberinto, heuristica):
    inicio = encontrar_posicion(laberinto, 'S')
    meta = encontrar_posicion(laberinto, 'G')

    abiertos = []
    f_inicial = 0
    elemento = (f_inicial, inicio)
    heapq.heappush(abiertos, elemento)

    g_costos = {inicio: 0}
    padre = {}
    cerrados = set()
    nodos_visitados = 0

    while len(abiertos) > 0:
        elemento = heapq.heappop(abiertos)
        actual = elemento[1]


        if actual in cerrados:
            continue

        cerrados.add(actual)
        nodos_visitados = nodos_visitados + 1

        # Camino parcial
        camino_parcial = []
        aux = actual
        while aux != inicio:
            camino_parcial.append(aux)
            aux = padre[aux]

        
        nodo_abiertos = []
        for elemento in abiertos:
            nodo = elemento[1]
            nodo_abiertos.append(nodo)
            
        mostrar_laberinto_aestrella(
            laberinto,
            nodo_abiertos,
            cerrados,
            camino_parcial
        )

        if actual == meta:
            break
        
        #metodo de relajación, si se llego a este nodo, y el nuevo camino es más barato, se toma ese
        for v in vecinos(laberinto, actual):
            nuevo_g = g_costos[actual] + costo_celda(laberinto, v)

            ya_esta_cerrado = v in cerrados #ya fue evaluado el nodo se usara como if para continuar con el algoritmo
            costo_guardado = g_costos.get(v, float('inf'))
            costo_nuevo = nuevo_g
            
            if ya_esta_cerrado and costo_nuevo >= costo_guardado:
                continue
                
            #se actualiza la información de las variables gracias al metodo de relajacion
            costo_anterior = g_costos.get(v, float('inf'))
            costo_nuevo = nuevo_g
            
            if nuevo_g < costo_anterior:
                #se guarda de donde viene el nodo o actualiza
                padre[v] = actual
                #Se actualiza el mejor costo conocido
                g_costos[v] = costo_nuevo
                #se recalcula la heuristica
                costo_estimado = heuristica(v, meta)
                f = costo_nuevo + costo_estimado
                heapq.heappush(abiertos, (f,v))
                

    # Reconstrucción del camino, es la misma que ucs
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
                #se cambio '.' a celda para que los 3 algoritmos puedan imprimir todos los simbolos
            elif pos in camino_set:
                print(GREEN + celda + RESET, end='') 
            else:
                print(GRAY + celda + RESET, end='')
        print()
        
#función para mostrar la impresión del A*, por que como pide un nuevo color, no podemos usar la función normal de mostrar laberinto por los colores
#es casi lo mismo que el otro mostrar, pero en este tenemos que ir mostrando los caminos parciales
def mostrar_laberinto_aestrella(laberinto, abiertos, cerrados, camino_parcial):
    abiertos = set(abiertos)
    cerrados = set(cerrados)
    camino_parcial = set(camino_parcial)

    for i, fila in enumerate(laberinto):
        for j, celda in enumerate(fila):
            pos = (i, j)

            if celda == 'S':
                print(YELLOW + 'S' + RESET, end='')

            elif celda == 'G':
                print(RED + 'G' + RESET, end='')

            elif pos in camino_parcial:
                print(GREEN + celda + RESET, end='')

            elif pos in abiertos:
                print(BLUE + celda + RESET, end='')

            elif pos in cerrados:
                print(GRAY + celda + RESET, end='')

            else:
                print(celda, end='')
        print()

    time.sleep(0.1)
    print("\n", end="")  #salto de linea para que se vea bonito
    

#Nuevo ejecutar para A*    
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


ejecutando = True
while ejecutando:
    print("\n=== Menú Principal ===")
    print("1) Resolver con BFS")
    print("2) Resolver con DFS")
    print("3) Resolver con UCS")
    print("4) A* con heurística Manhattan")
    print("5) A* con heurística Euclidiana")
    print("6) Cambiar laberinto (ruta de archivo)")
    print("7) Salir")
 
    opcion = input("Elige una opción: ")

    if opcion == '1':
        ejecutar(bfs, "BFS")

    elif opcion == '2':
        ejecutar(dfs, "DFS")
        
    elif opcion == '3':
        ejecutar(ucs, "UCS")

    elif opcion == '4':
        ejecutar_astar(heuristica_manhattan, "Manhattan")

    elif opcion == '5':
        ejecutar_astar(heuristica_euclidiana, "Euclidiana")
        
    elif opcion =='6':
        ruta = input("Ruta del archivo: ")
        try:
             with open(ruta, 'r') as f:
                 laberinto_actual = f.read().strip()
             print("Laberinto cargado correctamente.")
        except:
            print("Error al leer el archivo.")

    elif opcion == '7':
        print("Saliendo...")
        ejecutando = False

    else:
        print("Opción inválida.")
