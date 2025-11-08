import pygame
import random

pygame.init()
screen_height = 1080
screen_width = 1200
screen_delay = 30
count = 0 
highest_score = 0
pygame.mouse.set_cursor(*pygame.cursors.broken_x)
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shape cather GAme")

White = (255, 255, 255)
Red = (255, 0, 0)
Blue = (0, 0, 255)
Green = (0, 255, 0)

score = 0 
multiplier = 1
missed_circles = 0
font = pygame.font.Font(None, 36)
Falingspapep = []

def spawn_shape():
    shape_type = random.choice(['circle','rectangle'])
    color = random.choice([Red, Blue, Green])
    position = [random.randint(50, 1150), 0 ]
    size = random.randint(20, 50)

    return { 'type': shape_type,
             'color': color,
             'position': position,
             'size': size
            }
def draw_shape(shape):
    if shape['type'] == "circle":
        pygame.draw.circle(screen, shape['color'], shape['position'], shape['size'])
    elif shape['type'] == "rectangle":
        pygame.draw.rect(screen, shape['color'], (*shape['position'], shape['size'], shape['size']))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for shape in Falingspapep:
                if shape['type'] == 'rectangle':
                    if shape['position'][0]< x < shape['position'][0] + shape['size'] and \
                    shape['position'][1]< y < shape['position'][1] + shape['size']:
                        score -= 1
                        Falingspapep.remove(shape)
                if shape['type'] == 'circle':
                    distance = ((shape['position'][0] - x) ** 2 + (shape['position'][1] - y) ** 2) ** 0.5
                    if distance <= shape['size']:
                        score += 1
                        Falingspapep.remove(shape)
    screen.fill((255, 255, 255))
    if random.randint(1, 10) == 1:
        Falingspapep.append(spawn_shape())
    
    for shape in Falingspapep:
        shape['position'][1] += 5
        
        if shape['position'][1] > screen_height:
            Falingspapep.remove(shape)
            if missed_circles == 40:
                multiplier *= 2
            elif missed_circles == 60:
                multiplier *= 2
            elif missed_circles == 80:
                multiplier += 2
            
            if shape['type'] == 'circle':
                missed_circles += 1
                if shape['size'] > 20 and shape['size'] < 31:
                    score -= multiplier
                elif shape['size'] >= 31 and shape['size'] < 41:
                    score -= 3 * multiplier
                elif shape['size'] >= 41 and shape['size'] < 51:
                    score -= 5 * multiplier

    for shape in Falingspapep:
        draw_shape(shape)
    
    score_text = font.render(f'Score: {score}', True, (0, 0 ,0))
    missed_text = font.render(f'Missed circles: {missed_circles}', True, (0, 0 ,0))
    mult_text = font.render(f'Mult: x{multiplier}', True, (0, 0 ,0))
    screen.blit(score_text, (10, 10))
    screen.blit(missed_text, (10, 30))
    screen.blit(mult_text, (10, 50))

    if score < 0:
        running = False
    
    count += 1
    if count % 50 == 0:
        screen_delay -= 1

    if screen_delay < 20:
        screen_delay = 20
    if score > highest_score:
        highest_score = score
    pygame.display.flip()

    pygame.time.delay(screen_delay)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    Falingspapep.clear()
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 72)
    score_text = font.render('Game over!', True, (0, 0 ,0))
    mult_text = font.render(f'Your highest score is {highest_score}!', True, (0, 0 ,0))
    screen.blit(score_text, (450, 400))
    screen.blit(mult_text, (300, 500))
    pygame.display.flip()

# pygame.quit()
