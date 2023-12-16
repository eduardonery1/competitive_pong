import pygame  
import sys  
  
WIDTH, HEIGHT = (960,540)
  
pygame.init()    
    
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
clock = pygame.time.Clock()
FPS = 60 

RECT_WIDTH = 50
RECT_HEIGHT = 200
ID = 2

rect1 = pygame.Rect(5,HEIGHT/2 - RECT_HEIGHT/2,25,RECT_HEIGHT)
rect2 = pygame.Rect(WIDTH-30,HEIGHT/2 - RECT_HEIGHT/2,25,RECT_HEIGHT)

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
                   
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (255,0,255), rect1)
    pygame.draw.rect(screen, (0,255,255), rect2)


    pygame.display.update()