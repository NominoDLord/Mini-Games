########################################################################################################################
##                                                                                                                    ##
##       ##   ##   #####   ##    ##  ######  ##   ##   #####       #####        ##      #####   #####   #####         ##
##       ###  ##  ##   ##  ###  ###    ##    ###  ##  ##   ##      ##   ##      ##     ##   ##  ##  ##  ##   ##       ##
##       ## # ##  ##   ##  ## ## ##    ##    ## # ##  ##   ##      ##   ##      ##     ##   ##  #####   ##   ##       ##
##       ##  ###  ##   ##  ##    ##    ##    ##  ###  ##   ##      ##   ##      ##     ##   ##  ##  ##  ##   ##       ##
##       ##   ##   #####   ##    ##  ######  ##   ##   #####       #####        ######  #####   ##  ##  #####         ##
##                                                                                                                    ##
########################################################################################################################

import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_tablero(tablero):
    for fila in tablero:
        print(" | ".join(fila))
        print("-" * 17)

def verificar_ganador(tablero):
    # Verificar filas y columnas
    for i in range(3):
        if tablero[i][0] == tablero[i][1] == tablero[i][2] != ' ':
            return tablero[i][0]
        if tablero[0][i] == tablero[1][i] == tablero[2][i] != ' ':
            return tablero[0][i]

    # Verificar diagonales
    if tablero[0][0] == tablero[1][1] == tablero[2][2] != ' ':
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] != ' ':
        return tablero[0][2]

    return None

def tablero_lleno(tablero):
    for fila in tablero:
        if ' ' in fila:
            return False
    return True

def jugar_tic_tac_toe():
    jugador_actual = 'X'
    tablero = [['   ' for _ in range(3)] for _ in range(3)]

    while True:
        limpiar_pantalla()
        mostrar_tablero(tablero)

        fila = int(input(f"Jugador: {jugador_actual}, elige la fila (0, 1, 2): "))
        columna = int(input(f"Jugador: {jugador_actual}, elige la columna (0, 1, 2): "))

        if tablero[fila][columna] == ' ':
            tablero[fila][columna] = jugador_actual
            ganador = verificar_ganador(tablero)

            if ganador:
                limpiar_pantalla()
                mostrar_tablero(tablero)
                print(f"¡El jugador {ganador} ha ganado!")
                break
            elif tablero_lleno(tablero):
                limpiar_pantalla()
                mostrar_tablero(tablero)
                print("¡Empate!")
                break

            jugador_actual = 'O' if jugador_actual == 'X' else 'X'
        else:
            print("¡Casilla ocupada! Intenta de nuevo.")

if __name__ == "__main__":
    jugar_tic_tac_toe()
