########################################################################################################################
##                                                                                                                    ##
##       ##   ##   #####   ##    ##  ######  ##   ##   #####       #####        ##      #####   #####   #####         ##
##       ###  ##  ##   ##  ###  ###    ##    ###  ##  ##   ##      ##   ##      ##     ##   ##  ##  ##  ##   ##       ##
##       ## # ##  ##   ##  ## ## ##    ##    ## # ##  ##   ##      ##   ##      ##     ##   ##  #####   ##   ##       ##
##       ##  ###  ##   ##  ##    ##    ##    ##  ###  ##   ##      ##   ##      ##     ##   ##  ##  ##  ##   ##       ##
##       ##   ##   #####   ##    ##  ######  ##   ##   #####       #####        ######  #####   ##  ##  #####         ##
##                                                                                                                    ##
########################################################################################################################

# pip install pygame

import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)

# Configuración de la pantalla
ANCHO = 300
ALTO = 600
TAMANO_CUADRO = 30

# Definir formas de las piezas de Tetris
FORMAS = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [1]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [0, 1]],
    [[1, 1, 1], [1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
]

# Clase para representar el juego de Tetris
class Tetris:
    def __init__(self):
        self.tablero = [[0] * (ANCHO // TAMANO_CUADRO) for _ in range(ALTO // TAMANO_CUADRO)]
        self.pieza_actual = self.generar_pieza()
        self.pieza_x = 0
        self.pieza_y = 0

    def generar_pieza(self):
        forma = random.choice(FORMAS)
        color = random.choice([ROJO, VERDE, AZUL, CYAN, MAGENTA, AMARILLO, NARANJA])
        return {'forma': forma, 'color': color}

    def colision(self):
        for y, fila in enumerate(self.pieza_actual['forma']):
            for x, valor in enumerate(fila):
                if valor and (self.tablero[self.pieza_y + y][self.pieza_x + x] or
                              self.pieza_x + x < 0 or self.pieza_x + x >= ANCHO // TAMANO_CUADRO):
                    return True
        return False

    def actualizar_tablero(self):
        for y, fila in enumerate(self.pieza_actual['forma']):
            for x, valor in enumerate(fila):
                if valor:
                    self.tablero[self.pieza_y + y][self.pieza_x + x] = self.pieza_actual['color']

    def eliminar_lineas_completas(self):
        lineas_completas = [i for i, fila in enumerate(self.tablero) if all(fila)]
        for linea in lineas_completas:
            del self.tablero[linea]
            self.tablero.insert(0, [0] * (ANCHO // TAMANO_CUADRO))

    def rotar_pieza(self):
        nueva_forma = list(zip(*reversed(self.pieza_actual['forma'])))
        if self.pieza_x + len(nueva_forma[0]) <= ANCHO // TAMANO_CUADRO and not self.colision():
            self.pieza_actual['forma'] = nueva_forma

    def mover_pieza(self, direccion):
        nueva_x = self.pieza_x + direccion
        if 0 <= nueva_x < ANCHO // TAMANO_CUADRO and not self.colision():
            self.pieza_x = nueva_x

    def mover_abajo(self):
        nueva_y = self.pieza_y + 1
        if nueva_y + len(self.pieza_actual['forma']) <= ALTO // TAMANO_CUADRO and not self.colision():
            self.pieza_y = nueva_y
        else:
            self.actualizar_tablero()
            self.eliminar_lineas_completas()
            self.pieza_actual = self.generar_pieza()
            self.pieza_x = 0
            self.pieza_y = 0
            if self.colision():
                # Fin del juego
                pygame.quit()
                quit()

    def dibujar(self, pantalla):
        for y, fila in enumerate(self.tablero):
            for x, color in enumerate(fila):
                pygame.draw.rect(pantalla, color, [x * TAMANO_CUADRO, y * TAMANO_CUADRO, TAMANO_CUADRO, TAMANO_CUADRO])
        for y, fila in enumerate(self.pieza_actual['forma']):
            for x, valor in enumerate(fila):
                if valor:
                    pygame.draw.rect(pantalla, self.pieza_actual['color'],
                                     [(self.pieza_x + x) * TAMANO_CUADRO, (self.pieza_y + y) * TAMANO_CUADRO,
                                      TAMANO_CUADRO, TAMANO_CUADRO])


# Inicializar el juego
tetris = Tetris()

# Configurar la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Tetris')

# Bucle principal
reloj = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                tetris.mover_pieza(-1)
            elif event.key == pygame.K_RIGHT:
                tetris.mover_pieza(1)
            elif event.key == pygame.K_DOWN:
                tetris.mover_abajo()
            elif event.key == pygame.K_UP:
                tetris.rotar_pieza()

    pantalla.fill(NEGRO)
    tetris.mover_abajo()
    tetris.dibujar(pantalla)
    pygame.display.update()

    reloj.tick(5)  # Ajusta la velocidad del juego
