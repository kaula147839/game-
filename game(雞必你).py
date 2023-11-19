import pygame

FPS = 60
WHITE = (255,255,255)
WIDTH  = 500 
HEIGHT = 600  
#遊戲初始化 創視窗
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("雞弊你")
clock = pygame.time.Clock()

#迴圈
running = True
while running:
    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    #更新遊戲

    #畫面顯示
    screen.fill(WHITE)
    pygame.display.update()
pygame.quit() 