import pygame
import random

pygame.init()
clock = pygame.time.Clock()
fps = 60
screen_height = 768
screen_width = 865
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappybird")
bg_img = pygame.image.load('img/bg.png')

ground_img = pygame.image.load('img/ground.png')
groundscroll = 5
ground_x = 0
ground_y = 700
flying = False
gameover = False
bounce_force = -10
is_collided = False

White = (255, 255, 255)
Red = (255, 0, 0)
Blue = (0, 0, 255)
Green = (0, 255, 0)
score = 0 
font = pygame.font.Font(None, 36)
pipe = []
def restartfn():
    global score, gameover, flappy, bird_group
    bird_group.empty()
    pipe_group.empty()
    score = 0
    gameover = False

    flappy = Bird(100, int(screen_height / 2))
    bird_group.add(flappy)

    y = random.randint(200, 400)
    pipe = Pipe(screen_width, y, "top", False) 
    pipe_group.add(pipe)
    pipe = Pipe(screen_width, y, "bottom", False)
    pipe_group.add(pipe)
    

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        for i in range(1, 4):
            self.images.append(pygame.image.load(f'img/bird{i}.png'))
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.press = False
        self.counter = 0
        self.angle = 0
    
    def update(self):
        if flying == True:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < ground_y:
                self.rect.y += int(self.vel)

        if gameover == False:
            if pygame.key.get_pressed() [pygame.K_SPACE] and self.press == False:
                self.press = True
                self.vel = -12
            if not pygame.key.get_pressed() [pygame.K_SPACE]:
                self.press = False
                
            self.image = self.images[self.index]
            self.counter += 1
            if self.counter >= 10:
                self.index += 1
                self.counter = 0 
                if self.index > 2:
                    self.index = 0

            self.image = pygame.transform.rotate(self.image, self.vel * -2)


        
class Pipe (pygame.sprite.Sprite):
    def __init__(self, x, y, position, middle):
        pygame.sprite.Sprite.__init__(self)
        if middle == True:
            self.image = pygame.image.load('img/pipe2.png')
            self.pipe_gap = -490
        else:
            self.image = pygame.image.load('img/pipe.png')
            self.pipe_gap = random.randint(115, 250)

        self.position = position
        if position == 'top':
            self.image = pygame.transform.flip(self.image, 0, 1)
            self.rect = self.image.get_rect()
            self.rect.bottomleft = [x, y - int(self.pipe_gap / 2)]
        elif position == 'bottom':
            self.rect = self.image.get_rect()
            self.rect.topleft = [x, y + int(self.pipe_gap / 2)]

            
    def update(self):
        if flying == True:
            self.rect.x -= groundscroll
        if self.rect.left == 500 and self.position == "top":
            y = random.randint(70, 600)
            middle = random.choice([True, False, False, False])
            if middle == True:
                y = random.randint(int(screen_height / 2) -75,int(screen_height / 2) + 75)
            pipe = Pipe(screen_width, y, "top", middle) 
            pipe_group.add(pipe)
            pipe = Pipe(screen_width, y, "bottom", middle)
            pipe_group.add(pipe)
        elif self.rect.right < 0:
            self.kill()

class Button ():
    def _init_(self, x, y):
        self.x = x
        self.y = y
        self.restart = pygame.image.load('img/restart.png')
        self.restart_btn = pygame.transform.scale(self.restart,(250, 100))
        self.rect = self.restart_btn.get_rect()
    def draw(screen, self):
        pos = pygame.mouse.get_pos()
 
        screen.blit(self.restart_btn, (self.x, self.y))

        if self.rect.collidepoint(pos):
            restartfn()
       






bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
button = Button(int(screen_width / 2) - 100, int(ground_y / 2))



running = True
while running:
    screen.fill(White)   
    screen.blit(bg_img, (0,0))  

    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # running = False
        if flying == False and pygame.key.get_pressed() [pygame.K_SPACE]:
            flying = True
    ground_x -= groundscroll
    if ground_x < -25:
        ground_x = 0

    if is_collided == False and (pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top <= 0 or flappy.rect.bottom >= 700):
        is_collided = True
        if flappy.rect.top > 0:
            flappy.vel = bounce_force * 1
        if flappy.rect.bottom >= 700:
            flappy.rect.y += int(flappy.vel)
        gameover = True
        groundscroll = 0

    bird_group.draw(screen)
    pipe_group.draw(screen)

    if gameover == True:
        button.draw()
    
    bird_group.update()
    pipe_group.update()
    screen.blit(ground_img, (ground_x, ground_y))  

    pygame.display.flip()

pygame.quit()
