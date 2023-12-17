import pygame  
import sys  
  
WIDTH, HEIGHT = (1440,810)
RECT_WIDTH = 50
RECT_HEIGHT = HEIGHT / 3
BALL_RADIUS = 15

pygame.init()    
    
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
clock = pygame.time.Clock()
FPS = 60 


ID = 1

rect1 = pygame.Rect(5,HEIGHT/2 - RECT_HEIGHT/2,25,RECT_HEIGHT)
rect2 = pygame.Rect(WIDTH-30,HEIGHT/2 - RECT_HEIGHT/2,25,RECT_HEIGHT)
ball = pygame.Rect(WIDTH/2 - BALL_RADIUS, HEIGHT/2 - BALL_RADIUS, BALL_RADIUS*2, BALL_RADIUS*2)

background = pygame.image.load("./assets/background.png")


running = True
time = 0
while running: 
    dt = clock.tick(FPS) / 1000  # 'dt' will be the amount of seconds since last loop.
    time += dt
     
    for ev in pygame.event.get():  
        if ev.type == pygame.QUIT:  
            pygame.quit()  
            running = False

    x, y = (0,0)

    if time > 1:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            x = 0
            y = -5
        elif keys[pygame.K_DOWN]:
            x = 0
            y = 5

    if ID == 1:
        rect1.move_ip(x,y)
    elif ID==2:
        rect2.move_ip(x,y)
       
    #screen.fill((255,255,0))
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, (255,0,255), rect1)
    pygame.draw.rect(screen, (0,255,255), rect2)
    pygame.draw.rect(screen, (255,255,0), ball, border_radius=25)


    pygame.display.update()