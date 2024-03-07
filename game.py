import pygame
import random
import os
FPS = 60
WIDTH  = 500 
HEIGHT = 600  

WHITE = (255,255,255)
GREEN = (0, 255, 0)
GREY = (190,190,190)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)
#遊戲初始化 創視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("雞弊你")
clock = pygame.time.Clock()

#載入圖片
sky_img = pygame.image.load(os.path.join("img", "sky.png")).convert()
player1_img = pygame.image.load(os.path.join("img", "fighter-jet.png")).convert()
plane_img = pygame.image.load(os.path.join("img", "plane.png")).convert()
bullet_player1_img = pygame.image.load(os.path.join("img", "player1_bullet.png")).convert()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_plane():
    p = Plane()
    all_sprites.add(p)
    planes.add (p)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (hp/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
    


#輝船
class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(plane_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width *0.8 /2)
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(2,10)
        self.speedx = random.randrange(-5,4)
        


    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(2,10)
            self.speedx = random.randrange(-5,4)
     
#玩家
class Player1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player1_img,(50,38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect() 
        self.radius =20
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT- 90
        self.speedx = 10
        self.speedy = 10
        self.health = 100


    def update(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy
       


        if self.rect.left > WIDTH:
            self.rect.right = 0
        if self.rect.right < 0:
            self.rect.left = WIDTH 
        if self.rect.top < 0:
            self.rect.bottom = HEIGHT
        if self.rect.bottom >HEIGHT:
            self.rect.top = 0


    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
#組但
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_player1_img,(20,20))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10 

    def update(self):
       self.rect.y += self.speedy
       if self.rect.bottom < 0:
           self.kill() 

all_sprites = pygame.sprite.Group()
planes = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player1 = Player1()
all_sprites.add(player1)
for i in range(8):
    new_plane()
score = 0


#迴圈
running = True
while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player1.shoot()

    #更新遊戲
    all_sprites.update()   
    hits = pygame.sprite.groupcollide(planes, bullets, True,True)
    for hit in hits:
        score += 1
        new_plane()

    hits =  pygame.sprite.spritecollide(player1, planes, True ,pygame.sprite.collide_circle)
    for hit in hits:
        new_plane()
        player1.health -= hit.radius
        if player1.health <= 0:
            running = False
    #畫面顯示
    screen.fill(WHITE)
    screen.blit(sky_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score),18,WIDTH/2,10)
    draw_health(screen,player1.health,5 ,10 )
    pygame.display.update()
pygame.quit() 