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
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("雞星人進攻")
clock = pygame.time.Clock()

#載入圖片
sky_img = pygame.image.load(os.path.join("img", "universe1.png")).convert()
player1_img = pygame.image.load(os.path.join("img", "UFO.png")).convert()
player1_mini_img = pygame.transform.scale(player1_img,(30,30))
player1_mini_img.set_colorkey(WHITE)
pygame.display.set_icon(player1_mini_img)
plane_img = pygame.image.load(os.path.join("img", "monster.png")).convert()
bullet_player1_img = pygame.image.load(os.path.join("img", "egg.png")).convert()
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player1'] = []
for i in range(5):
    expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(WHITE)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75,75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (75,75)))
    player1_expl_img = pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    player1_expl_img.set_colorkey(WHITE)
    expl_anim['player1'].append(pygame.transform.scale(expl_img, (80,80)))
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield_2D.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "moreegg.png")).convert()
# #載入音樂
# shoot_sound = pygame.mixer.Sound(os.path.join("路徑"))
# expl_sounds = [
#     pygame.mixer.Sound(os.path.join("路徑")),
#     pygame.mixer.Sound(os.path.join("路徑"))
# ]
# pygame.mixer.music.load(os.path.join("路徑"))
# pygame.mixer.music.set_volune(0.4)


#輸入字串
font_name =os.path.join("mingliu.ttc")
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

#畫生命條
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
    
def draw_lives(surf, lives, img,x ,y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y 
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(sky_img,(0,0))
    draw_text(screen, '雞星人進攻', 50 , WIDTH/2 , HEIGHT/4)
    draw_text(screen, '上下左右鍵控制UFO', 50 , WIDTH/2 , HEIGHT/2)
    draw_text(screen, '任意鍵開始遊戲', 50 , WIDTH/2 , HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False
#輝船
class Plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(plane_img,(70,70))
        self.image.set_colorkey(WHITE)
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
        self.image = pygame.transform.scale(player1_img,(60,60))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect() 
        self.radius =20
        #pygame.draw.circle(self.image,RED,self.rect.center,self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT- 90
        self.speedx = 10
        self.speedy = 10
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0


    def update(self):
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now  

        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT- 90


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
           self.rect.top = 0
        #if self.rect.bottom > HEIGHT:
        #   self.rect.bottom = HEIGHT
            


    def shoot(self):
        if not(self.hidden):
            # shoot_sound.play()
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)


    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
       self.gun += 1
       self.gun_time = pygame.time.get_ticks()
#組但
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_player1_img,(30,30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10 

    def update(self):
       self.rect.y += self.speedy
       if self.rect.bottom < 0:
           self.kill() 
#爆炸
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
#能力
class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = power_imgs[self.type]
        self.image = pygame.transform.scale(power_imgs[self.type], (30, 30))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
       self.rect.y += self.speedy
       if self.rect.top > HEIGHT:
           self.kill() 



#迴圈
show_init = True
running = True
while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        planes = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player1 = Player1()
        all_sprites.add(player1)
        for i in range(8):
            new_plane()
        score = 0
        # pygame.mixer.music.play(-1)

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
    #判斷石頭 子彈相撞
    hits = pygame.sprite.groupcollide(planes, bullets, True,True)
    for hit in hits:
        score += 1
        # random.choice(expl_sounds).play
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.4:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)

        new_plane()
    #判斷石頭 飛船相撞
    hits =  pygame.sprite.spritecollide(player1, planes, True ,pygame.sprite.collide_circle)
    for hit in hits:
        new_plane()
        player1.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player1.health <= 0:
            death_expl = Explosion(player1.rect.center,'player1')
            all_sprites.add(death_expl)
            player1.lives -= 1
            player1.health = 100
            player1.hide()

    #判斷寶物 飛船相撞
    hits =  pygame.sprite.spritecollide(player1, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player1.health += 20
            if player1.health > 100:
                player1.health = 100
        if hit.type == 'gun':
            player1.gunup()
    if player1.lives == 0 and not(death_expl.alive()):
        show_init = True

    #畫面顯示
    screen.fill(WHITE)
    screen.blit(sky_img,(0,0))
    all_sprites.draw(screen)
    draw_text(screen, str(score),18,WIDTH/2,10)
    draw_health(screen,player1.health,5 ,10 )
    draw_lives(screen, player1.lives, player1_mini_img, WIDTH - 100, 15)
    pygame.display.update()
pygame.quit() 