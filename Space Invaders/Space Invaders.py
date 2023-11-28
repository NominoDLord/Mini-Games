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
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Jugador
player_size = 50
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - 2 * player_size
player_speed = 5

# Enemigos
enemy_size = 50
enemy_speed = 2
enemies = []

# Disparo
bullet_size = 5
bullet_speed = 7
bullets = []

# Función para dibujar al jugador en la pantalla
def draw_player(x, y):
    pygame.draw.rect(screen, white, [x, y, player_size, player_size])

# Función para dibujar a los enemigos en la pantalla
def draw_enemy(x, y):
    pygame.draw.rect(screen, red, [x, y, enemy_size, enemy_size])

# Función para dibujar un proyectil en la pantalla
def draw_bullet(x, y):
    pygame.draw.rect(screen, white, [x, y, bullet_size, bullet_size])

# Ciclo principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Manejo de la entrada del jugador
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            elif event.key == pygame.K_RIGHT:
                player_x += player_speed
            elif event.key == pygame.K_SPACE:
                bullets.append([player_x + player_size // 2, player_y])

    # Mover al jugador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += player_speed

    # Mover a los enemigos
    for enemy in enemies:
        enemy[1] += enemy_speed

    # Generar nuevos enemigos aleatorios
    if random.randint(0, 100) < 5:
        enemy_x = random.randint(0, screen_width - enemy_size)
        enemy_y = 0
        enemies.append([enemy_x, enemy_y])

    # Mover proyectiles
    for bullet in bullets:
        bullet[1] -= bullet_speed

    # Eliminar proyectiles fuera de la pantalla
    bullets = [bullet for bullet in bullets if bullet[1] > 0]

    # Colisiones entre proyectiles y enemigos
    new_enemies = []
    for enemy in enemies:
        hit_enemies = [bullet for bullet in bullets if (
            bullet[0] < enemy[0] + enemy_size and
            bullet[0] + bullet_size > enemy[0] and
            bullet[1] < enemy[1] + enemy_size and
            bullet[1] + bullet_size > enemy[1]
        )]
        if not hit_enemies:
            new_enemies.append(enemy)

    enemies = new_enemies

    # Dibujar en la pantalla
    screen.fill(black)
    draw_player(player_x, player_y)
    for enemy in enemies:
        draw_enemy(enemy[0], enemy[1])
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1])

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    pygame.time.Clock().tick(60)
