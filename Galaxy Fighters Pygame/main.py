import pygame
import os
import time
import random

pygame.font.init()
pygame.mixer.init()

HEALTH_FONT = pygame.font.SysFont('roboto', 40)
WINNER_FONT = pygame.font.SysFont('roboto', 100)


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galaxy Fighters")

BG = pygame.transform.scale(pygame.image.load("Assets/space.png"), (WIDTH, HEIGHT))

clock = pygame.time.Clock()
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 50

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACSHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACSHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACSHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

RED_SPACSHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACSHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACSHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'GUN+Silencer.mp3'))

def draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(BG, (0,0))
    pygame.draw.rect(WIN, (0,0,0), BORDER)

    for bullet in red_bullets:
        pygame.draw.rect(WIN, "red", bullet)
    
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, "yellow", bullet)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, "white")
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, "yellow")

    WIN.blit(red_health_text, (10, 10))
    WIN.blit(yellow_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(RED_SPACSHIP, red)
    WIN.blit(YELLOW_SPACSHIP, yellow)

    pygame.display.update()

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:
            red.x-= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x:
        red.x+= VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:
        red.y-= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT:
        red.y+= VEL

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VEL > BORDER.x + BORDER.width:
            yellow.x-= VEL
    if keys_pressed[pygame.K_RIGHT]  and yellow.x + yellow.width + VEL < WIDTH + BORDER.width:
        yellow.x+= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + VEL + yellow.height < HEIGHT:
        yellow.y+= VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0:
        yellow.y-= VEL

def handle_bullets(red_bullets, yellow_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
            
    
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, "white")
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    run = True

    red = pygame.Rect(WIDTH/6, HEIGHT/2.5, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(WIDTH*4.5/6, HEIGHT/2.5, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10


    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LALT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_RALT and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
                
        winner_text = ""
        if red_health <= 0:
            winner_text = "YELLOW WINS"
        
        if yellow_health <= 0:
            winner_text = "RED WINS"

        if winner_text != "":
            draw_winner(winner_text)
            break

        draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        yellow_handle_movement(keys_pressed, yellow)

        handle_bullets(red_bullets, yellow_bullets, red, yellow)
        

    main()

if __name__ == "__main__":
    main()


'''
Reference: TechwithTim
'''