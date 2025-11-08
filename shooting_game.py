import pygame
import random

pygame.init()

screen_height = 800
screen_width = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shooter Game")

White = (255, 255, 255)
Red = (255, 0, 0)
Blue = (0, 0, 255)
Green = (0, 255, 0)
Black = (0, 0, 0)

player_img = pygame.image.load('player.png')
player_img = pygame.transform.scale(player_img, (30, 30))
player_size = 30
enemy_size = 50
bullet_size = 30
frenemy_img = pygame.image.load('frenemy.png')
frenemy_img = pygame.transform.scale(frenemy_img, (50, 50))
bullet_img = pygame.image.load('bullet.png')
bullet_img = pygame.transform.scale(bullet_img, (30,30))

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)

pygame.display.flip()

def reset_game():
    global player_x, bullets, frenemies, score, frenemy_spawn_timer
    player_x = screen_width // 2 - 25

    bullets = []
    frenemies = []

    for _ in range(4):
        x = random.randint(0, screen_width - 40)
        frenemies.append({'x': x, 'y': -50, 'speed': 1})

    score = 0

    frenemy_spawn_timer = 0

reset_game()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            bullets.append({'x': player_x, 'y': screen_height - 100})
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            reset_game()
    
    # if event.type == pygame.KEYDOWN and event.key == pygame.K_a and player_x >= 5:
    #     player_x -= 5
    # if event.type == pygame.KEYDOWN and event.key == pygame.K_d and player_x <= screen_width - 5:
    #     player_x += 5

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x > 0:
        player_x -= 5
    if keys[pygame.K_d] and player_x < screen_width - player_size:
        player_x += 5

    for bullet in bullets:
        bullet['y'] -= 10
        if bullet ['y'] < 0:
            bullets.remove(bullet)
        
    
    for frenemy in frenemies:
        frenemy['y'] += frenemy['speed']
        if frenemy ['y'] > screen_height:
            frenemies.remove(frenemy)
            score -= 10

        
        for bullet in bullets:
            if ((frenemy['x'] + enemy_size >= bullet['x'] and frenemy['x'] <= bullet['x'] or frenemy['x'] + enemy_size >= bullet['x'] + bullet_size and frenemy['x'] <= bullet['x'] + bullet_size)  and bullet['y'] <= frenemy['y'] + 40):
                if frenemy ['y'] < (screen_height - 100):
                    # screen.blit(bullet_img,(bullet['x'], bullet['y']))
                    # screen.blit(frenemy_img,(frenemy['x'], frenemy['y']))
                    # draw_rect = pygame.Rect(frenemy['x'] - bullet_size, frenemy['y'] + enemy_size + bullet_size, frenemy['x'] + enemy_size + (bullet_size * 2), enemy_size + bullet_size)
                    # pygame.display.update(draw_rect)
                    bullets.remove(bullet)
                    frenemies.remove(frenemy)
                    score += 1
                    break
    frenemy_spawn_timer += 1    
    if frenemy_spawn_timer > random.randint(80, 120) and len(frenemies) < 10:
        x = random.randint(0, screen_width - enemy_size)
        frenemies.append ({'x': x, 'y': -50, 'speed': random.randint(1, 5)})
        frenemy_spawn_timer = 0
        
    screen.fill(White)

    screen.blit(player_img, (player_x, screen_height - 100))
    
    for frenemy in frenemies:
        screen.blit(frenemy_img,(frenemy['x'], frenemy['y']))

    for bullet in bullets:
        screen.blit(bullet_img,(bullet['x'], bullet['y']))

    score_text = font.render(f"Score: {score}", True, Black)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()


    clock.tick(60)

pygame.quit()
