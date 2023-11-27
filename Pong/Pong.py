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

import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
ANCHO, ALTO = 600, 400
FPS = 60

# Definir colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Configuración de las paletas y la pelota
PALETA_ANCHO, PALETA_ALTO = 10, 60
PELOTA_RADIO = 10

# Configuración de la velocidad de movimiento
VELOCIDAD = 5

# Clase para representar la paleta
class Paleta(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PALETA_ANCHO, PALETA_ALTO))
        self.image.fill(BLANCO)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def mover(self, dy):
        self.rect.y += dy
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > ALTO:
            self.rect.bottom = ALTO

# Clase para representar la pelota
class Pelota(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PELOTA_RADIO * 2, PELOTA_RADIO * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLANCO, (PELOTA_RADIO, PELOTA_RADIO), PELOTA_RADIO)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocidad = [VELOCIDAD, VELOCIDAD]

    def mover(self):
        self.rect.x += self.velocidad[0]
        self.rect.y += self.velocidad[1]

        # Rebote en los bordes izquierdo y derecho de la pantalla
        if self.rect.left < 0 or self.rect.right > ANCHO:
            self.velocidad[0] = -self.velocidad[0]

        # Rebote en los bordes superior e inferior de la pantalla
        if self.rect.top < 0 or self.rect.bottom > ALTO:
            self.velocidad[1] = -self.velocidad[1]

# Inicializar el juego
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Pong')

reloj = pygame.time.Clock()

paleta_jugador = Paleta(30, ALTO // 2)
paleta_cpu = Paleta(ANCHO - 30, ALTO // 2)
pelota = Pelota(ANCHO // 2, ALTO // 2)

# Marcadores
puntos_jugador = 0
puntos_cpu = 0
fuente = pygame.font.Font(None, 36)

# Grupos de sprites
todos_los_sprites = pygame.sprite.Group()
todos_los_sprites.add(paleta_jugador, paleta_cpu, pelota)

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento de la paleta del jugador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP]:
        paleta_jugador.mover(-VELOCIDAD)
    if teclas[pygame.K_DOWN]:
        paleta_jugador.mover(VELOCIDAD)

    # Movimiento de la paleta de la CPU (simulación simple)
    if pelota.velocidad[0] > 0:
        if pelota.rect.centery < paleta_cpu.rect.centery:
            paleta_cpu.mover(-VELOCIDAD)
        elif pelota.rect.centery > paleta_cpu.rect.centery:
            paleta_cpu.mover(VELOCIDAD)

    # Movimiento de la pelota
    pelota.mover()

    # Colisiones con las paletas
    if pygame.sprite.collide_rect(paleta_jugador, pelota) or pygame.sprite.collide_rect(paleta_cpu, pelota):
        pelota.velocidad[0] = -pelota.velocidad[0]

    # Puntos
    if pelota.rect.left < 0:
        puntos_cpu += 1
        pelota.rect.center = (ANCHO // 2, ALTO // 2)
    elif pelota.rect.right > ANCHO:
        puntos_jugador += 1
        pelota.rect.center = (ANCHO // 2, ALTO // 2)

    # Dibujar en la pantalla
    pantalla.fill(NEGRO)
    todos_los_sprites.draw(pantalla)

    # Dibujar los marcadores
    texto_jugador = fuente.render(str(puntos_jugador), True, BLANCO)
    texto_cpu = fuente.render(str(puntos_cpu), True, BLANCO)
    pantalla.blit(texto_jugador, (ANCHO // 4, 20))
    pantalla.blit(texto_cpu, (3 * ANCHO // 4 - fuente.size(str(puntos_cpu))[0], 20))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    reloj.tick(FPS)
