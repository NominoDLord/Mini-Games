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
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 600, 600
TAMANO_CELDA = 30
FPS = 10

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AMARILLO = (255, 255, 0)

# Direcciones
ARRIBA = (0, -1)
ABAJO = (0, 1)
IZQUIERDA = (-1, 0)
DERECHA = (1, 0)

# Clase para representar el juego de Pac-Man
class PacmanGame:
    def __init__(self):
        self.pacman = [3, 3]
        self.fantasmas = [[8, 8], [12, 12]]
        self.puntaje = 0
        self.tablero = [[0] * (ANCHO // TAMANO_CELDA) for _ in range(ALTO // TAMANO_CELDA)]
        self.crear_tablero()
        self.direccion = DERECHA

    def crear_tablero(self):
        # Crear paredes
        for i in range(ALTO // TAMANO_CELDA):
            self.tablero[i][0] = 1
            self.tablero[i][-1] = 1
        for i in range(ANCHO // TAMANO_CELDA):
            self.tablero[0][i] = 1
            self.tablero[-1][i] = 1

        # Crear puntos
        for i in range(1, (ANCHO // TAMANO_CELDA) - 1):
            for j in range(1, (ALTO // TAMANO_CELDA) - 1):
                if random.random() > 0.9:
                    self.tablero[j][i] = 2

        # Posicionar Pac-Man
        self.tablero[self.pacman[1]][self.pacman[0]] = 3

        # Posicionar fantasmas
        for fantasma in self.fantasmas:
            self.tablero[fantasma[1]][fantasma[0]] = 4

    def mover_pacman(self):
        nueva_posicion = [self.pacman[0] + self.direccion[0], self.pacman[1] + self.direccion[1]]
        if self.tablero[nueva_posicion[1]][nueva_posicion[0]] != 1:
            self.tablero[self.pacman[1]][self.pacman[0]] = 0
            self.pacman = nueva_posicion
            self.tablero[self.pacman[1]][self.pacman[0]] = 3

            if self.tablero[self.pacman[1]][self.pacman[0]] == 2:
                self.puntaje += 10
                self.tablero[self.pacman[1]][self.pacman[0]] = 0

    def mover_fantasmas(self):
        for fantasma in self.fantasmas:
            direccion_fantasma = random.choice([ARRIBA, ABAJO, IZQUIERDA, DERECHA])
            nueva_posicion = [fantasma[0] + direccion_fantasma[0], fantasma[1] + direccion_fantasma[1]]

            if self.tablero[nueva_posicion[1]][nueva_posicion[0]] != 1:
                self.tablero[fantasma[1]][fantasma[0]] = 0
                fantasma[0], fantasma[1] = nueva_posicion[0], nueva_posicion[1]
                self.tablero[fantasma[1]][fantasma[0]] = 4

    def verificar_colision(self):
        if self.pacman in self.fantasmas:
            pygame.quit()
            sys.exit()

    def dibujar(self, pantalla):
        pantalla.fill(NEGRO)

        for y, fila in enumerate(self.tablero):
            for x, valor in enumerate(fila):
                if valor == 1:
                    pygame.draw.rect(pantalla, BLANCO, [x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA])
                elif valor == 2:
                    pygame.draw.circle(pantalla, AMARILLO,
                                       [x * TAMANO_CELDA + TAMANO_CELDA // 2, y * TAMANO_CELDA + TAMANO_CELDA // 2],
                                       TAMANO_CELDA // 6)
                elif valor == 3:
                    pygame.draw.circle(pantalla, AMARILLO,
                                       [x * TAMANO_CELDA + TAMANO_CELDA // 2, y * TAMANO_CELDA + TAMANO_CELDA // 2],
                                       TAMANO_CELDA // 2)
                elif valor == 4:
                    pygame.draw.rect(pantalla, BLANCO, [x * TAMANO_CELDA, y * TAMANO_CELDA, TAMANO_CELDA, TAMANO_CELDA])

        pygame.display.flip()

# Inicializar el juego
juego = PacmanGame()

# Configurar la pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Pac-Man')

# Bucle principal
reloj = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                juego.direccion = ARRIBA
            elif event.key == pygame.K_DOWN:
                juego.direccion = ABAJO
            elif event.key == pygame.K_LEFT:
                juego.direccion = IZQUIERDA
            elif event.key == pygame.K_RIGHT:
                juego.direccion = DERECHA

    juego.mover_pacman()
    juego.mover_fantasmas()
    juego.verificar_colision()
    juego.dibujar(pantalla)

    pygame.display.update()
    reloj.tick(FPS)
