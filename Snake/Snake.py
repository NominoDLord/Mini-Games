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
import time
import random

pygame.init()

# Configuración del juego
WIDTH, HEIGHT = 800, 600
SNAKE_SIZE = 20
FPS = 15

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Inicialización de la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 50)

def snake(snake_size, snake_list):
    for x, y in snake_list:
        pygame.draw.rect(screen, GREEN, [x, y, snake_size, snake_size])

def message(msg, color):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, [WIDTH / 6, HEIGHT / 3])

def game_loop():
    game_over = False
    game_close = False

    # Inicialización de la serpiente
    snake_list = []
    snake_length = 1

    # Posición y velocidad inicial de la serpiente
    lead_x, lead_y = WIDTH / 2, HEIGHT / 2
    lead_x_change, lead_y_change = 0, 0

    # Posición inicial de la comida
    food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
    food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0

    while not game_over:

        while game_close:
            screen.fill(WHITE)
            message("You Lost! Press C-Play Again or Q-Quit", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -SNAKE_SIZE
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = SNAKE_SIZE
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -SNAKE_SIZE
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = SNAKE_SIZE
                    lead_x_change = 0

        # Actualizar la posición de la serpiente
        lead_x += lead_x_change
        lead_y += lead_y_change

        # Verificar colisiones
        if lead_x >= WIDTH or lead_x < 0 or lead_y >= HEIGHT or lead_y < 0:
            game_close = True

        # Actualizar la pantalla
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, [food_x, food_y, SNAKE_SIZE, SNAKE_SIZE])
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        snake(SNAKE_SIZE, snake_list)

        pygame.display.update()

        # Verificar si la serpiente come la comida
        if lead_x == food_x and lead_y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 20.0) * 20.0
            food_y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 20.0) * 20.0
            snake_length += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

game_loop()
