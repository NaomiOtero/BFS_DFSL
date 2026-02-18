import math

def imprimir_tablero(tablero):

    print(" " + tablero[0] + " | " + tablero[1] + " | " + tablero[2])
    print("---|---|---")
    print(" " + tablero[3] + " | " + tablero[4] + " | " + tablero[5])
    print("---|---|---")
    print(" " + tablero[6] + " | " + tablero[7] + " | " + tablero[8])


def verificar_ganador(tablero):

    combinaciones = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for combinacion in combinaciones:

        a = combinacion[0]
        b = combinacion[1]
        c = combinacion[2]

        if tablero[a] == tablero[b] and tablero[b] == tablero[c]:
            if tablero[a] != " ":
                return tablero[a]

    if " " not in tablero:
        return "Empate"

    return None



# ==============================
# Minimax con Poda Alfa-Beta
# ==============================

def minimax(tablero, es_maximizador, alpha, beta):
    resultado = verificar_ganador(tablero)

    if resultado == "O":
        return 1
    elif resultado == "X":
        return -1
    elif resultado == "Empate":
        return 0

    if es_maximizador:
        mejor = -math.inf

        for i in range(9):
            if tablero[i] == " ":
                tablero[i] = "O"
                valor = minimax(tablero, False, alpha, beta)
                tablero[i] = " "

                mejor = max(mejor, valor)
                alpha = max(alpha, mejor)

                if beta <= alpha:
                    break

        return mejor

    else:
        mejor = math.inf

        for i in range(9):
            if tablero[i] == " ":
                tablero[i] = "X"
                valor = minimax(tablero, True, alpha, beta)
                tablero[i] = " "

                mejor = min(mejor, valor)
                beta = min(beta, mejor)


                if beta <= alpha:
                    break

        return mejor


def mejor_movimiento(tablero):

    mejor_valor = -math.inf
    mejor_posicion = None

    for posicion in range(9):

        if tablero[posicion] == " ":

            # Simulamos jugada
            tablero[posicion] = "O"

            # Evaluamos
            resultado = minimax(tablero, False, -math.inf, math.inf)

            # Deshacemos jugada
            tablero[posicion] = " "

            # Comparamos resultados
            if resultado > mejor_valor:
                mejor_valor = resultado
                mejor_posicion = posicion

    return mejor_posicion



def jugar():
    while True:
        tablero = [" "] * 9
        print("\n===== NUEVA PARTIDA =====\n")

        while True:
            imprimir_tablero(tablero)

            # Turno jugador
            while True:
                try:
                    pos = int(input("Elige una posición (1-9): ")) - 1
                    if pos < 0 or pos > 8:
                        print("Número inválido.")
                        continue
                    if tablero[pos] != " ":
                        print("Casilla ocupada.")
                        continue
                    break
                except:
                    print("Entrada inválida.")

            tablero[pos] = "X"

            resultado = verificar_ganador(tablero)
            if resultado:
                imprimir_tablero(tablero)
                print(f"\nResultado: {resultado}")
                break

            # Turno IA
            print("\nMovimiento de la IA(O)\n")
            movimiento = mejor_movimiento(tablero)
            tablero[movimiento] = "O"

            resultado = verificar_ganador(tablero)
            if resultado:
                imprimir_tablero(tablero)
                print(f"\nEl ganador es: {resultado}")
                break

        opcion = ""
        while opcion != "s" and opcion != "n":
            opcion = input("\n¿Quieres volver a jugar? (S/N): ").lower()
            if opcion == "s":
                print("Nueva partida iniciada\n")
            elif opcion == "n":
                print("Gracias por jugar")
                return
            else:
                print("Opción inválida.")


jugar()
