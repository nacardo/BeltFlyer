"""
Created May 1, 2021

@author Nicholas Cardoza
"""

import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 840

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # tuple, caps for constants
pygame.display.set_caption("Belt Flyer!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 50)
ORANGE = (255, 215, 0)

# sound for collision
HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'small_explosion.mp3'))

FONT = pygame.font.SysFont('arial', 20)
LOSER_FONT = pygame.font.SysFont('arial', 40)
WINNER_FONT = pygame.font.SysFont('arial', 80)

FPS = 60
VEL = 5
GRAV = 2.5

# make hit equal to user event value
HIT = pygame.USEREVENT


# load image in and convert to alpha for better performance
def loadify(img):
    return pygame.image.load(img).convert_alpha()


# image for user ship
SHIP_WIDTH, SHIP_HEIGHT = 120, 100
SHIP_IMAGE = loadify((os.path.join(
    'Assets', 'ship.png')))
SHIP = pygame.transform.scale(SHIP_IMAGE,
                              (SHIP_WIDTH, SHIP_HEIGHT))

# image for ship exhaust
FLAMES_IMAGE = loadify((os.path.join(
    'Assets', 'flames.png')))
FLAMES = pygame.transform.rotate(pygame.transform.scale(FLAMES_IMAGE,
                                                        (SHIP_WIDTH // 2, SHIP_HEIGHT // 2)), 180)

# image for asteroid
ROCK_WIDTH, ROCK_HEIGHT = 60, 60
ROCK_IMAGE = loadify((os.path.join(
    'Assets', 'asteroid.png')))
ROCK = pygame.transform.scale(ROCK_IMAGE,
                              (ROCK_WIDTH, ROCK_HEIGHT))

# image for background
SPACE = pygame.transform.scale(loadify(
    os.path.join('Assets', 'orion.jpg')), (WIDTH, HEIGHT))

# image for winner background
WINNER_BG = pygame.transform.scale(loadify(
    os.path.join('Assets', 'rosette.jpg')), (WIDTH, HEIGHT))

# image of keyboard for controls info
CONTROLS_IMAGE = pygame.transform.scale(loadify(
    os.path.join('Assets', 'controls.png')), (500, 180))


# main draw function
def draw_window(ship, obstacles):
    WIN.fill(GRAY)
    WIN.blit(SPACE, (0, 0))
    WIN.blit(FLAMES, (ship.x + 5, ship.y + SHIP_HEIGHT - 30))
    WIN.blit(SHIP, (ship.x - (SHIP_WIDTH * .2), ship.y))
    for obstacle in obstacles:
        WIN.blit(ROCK, (obstacle.x, obstacle.y))
    pygame.display.update()


# control the ship
def ship_control(keys_pressed, ship):
    if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and ship.x > 0:
        ship.x -= VEL
    if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and ship.x + VEL + ship.width < WIDTH:  # RIGHT
        ship.x += VEL
    if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and ship.y - VEL > 0:  # UP
        ship.y -= VEL
    if ship.y + SHIP_HEIGHT < HEIGHT:
        ship.y += GRAV


# check if asteroids hit ship
def handle_obstacles(obstacles, ship):
    for obstacle in obstacles:
        obstacle.y += GRAV
        if ship.colliderect(obstacle):
            obstacles.remove(obstacle)
            pygame.event.post(pygame.event.Event(HIT))
        elif obstacle.y > HEIGHT:
            obstacles.remove(obstacle)


# display score, health, and difficulty
def info_text(text1, text2, text3):
    draw_text1 = FONT.render(text1, 1, ORANGE)
    draw_text2 = FONT.render(text2, 1, ORANGE)
    draw_text3 = FONT.render(text3, 1, ORANGE)
    # need to change these to be more (fitting to change)
    WIN.blit(draw_text1, (10, 20))
    # need to change these to be more (fitting to change)
    WIN.blit(draw_text2, (10, 40))
    WIN.blit(draw_text3, (10, 60))
    pygame.display.update()


# display keyboard controls
def draw_intro(text):
    WIN.fill(BLACK)
    WIN.blit(CONTROLS_IMAGE,
             (WIDTH // 2 - CONTROLS_IMAGE.get_width() // 2, HEIGHT // 2))
    text_y = 200
    draw_text = LOSER_FONT.render(str(text), 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, text_y))
    text_y += draw_text.get_height()
    pygame.display.update()
    pygame.time.delay(5000)


# loser screen
def draw_loser(text):
    WIN.fill(GRAY)
    WIN.blit(SPACE, (0, 0))
    text_y = HEIGHT // 2 - 200
    for line in text:
        draw_text = LOSER_FONT.render(str(line), 1, WHITE)
        WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, text_y))
        text_y += draw_text.get_height()
    pygame.display.update()
    pygame.time.delay(5000)


# winner screen
def draw_winner(text):
    WIN.blit(WINNER_BG, (0, 0))
    text_y = HEIGHT // 2 - 200
    draw_text = WINNER_FONT.render(str(text), 1, WHITE)
    WIN.blit(draw_text, (WIDTH // 2 - draw_text.get_width() // 2, text_y))
    text_y += draw_text.get_height()
    pygame.display.update()
    pygame.time.delay(5000)


#  main loop
def main():
    # create ship hit box
    ship = pygame.Rect(WIDTH // 2 - (SHIP_WIDTH * .6) // 2,
                       HEIGHT - SHIP_HEIGHT, SHIP_WIDTH * .6, SHIP_HEIGHT)
    score, health = 0, 5

    cooldown = 800  # number of ticks between obstacles
    last = 0  # used for keeping track of ticks
    difficultly = 12  # max number of asteroids on screen
    obstacles = []
    clock = pygame.time.Clock()
    run = True
    draw_intro("Use the keys shown below to control the ship.")
    while run:
        clock.tick(FPS)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # quit if x
                pygame.quit()
            if event.type == HIT:  # if there is a collision
                HIT_SOUND.play()
                health -= 1

        # if number of asteroids on screen is less than difficulty
        if len(obstacles) < difficultly:

            if now - last >= cooldown:
                last = now
                obstacle = pygame.Rect(
                    random.randint(0, WIDTH - ROCK_WIDTH), -10, ROCK_WIDTH, ROCK_HEIGHT)
                obstacles.append(obstacle)

        # if player is dead
        if health <= 0:
            loser_text = ['Your ship has been destroyed.',
                          f'Distance left: {150 - round(score, 2)} million km']

            draw_loser(loser_text)
            run = False

        if score >= 150:
            draw_winner("You made it through the belt!")
            run = False

        health_text = f'Health: {health}'

        # increment score
        score += .02

        # check if any key are being pressed
        keys_pressed = pygame.key.get_pressed()

        ship_control(keys_pressed, ship)
        handle_obstacles(obstacles, ship)
        draw_window(ship, obstacles)
        info_text(health_text,
                  f'Difficulty: {difficultly}', f'Distance: {round(score, 2)}')

    main()


if __name__ == '__main__':
    main()
