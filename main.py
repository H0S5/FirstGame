from re import T
from turtle import color, width
import pygame
import os
pygame.font.init()

HEALTH_FONT=pygame.font.SysFont('comicsans',40)
WINNER_FONT=pygame.font.SysFont('comicsans',100)
WIDTH,HEIGHT=900,500
WIN  = pygame.display.set_mode((WIDTH,HEIGHT))
BORDER=pygame.Rect(WIDTH//2 -5, 0 ,10,HEIGHT)
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
DARK_BLUE=(11,11,69)

MAX_BULLETS=3
pygame.display.set_caption("First Game")
FPS = 60
VELOCITY=5

RED_HIT=pygame.USEREVENT +1
YELLOW_HIT=pygame.USEREVENT +2

YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))
YELLOW_SPACESHIP=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(55,40)),90)

RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP=pygame.transform.rotate (pygame.transform.scale(RED_SPACESHIP_IMAGE,(55,40)),-90)

SPACE_IMAGE=pygame.transform.scale (pygame.image.load(os.path.join('Assets','space.png')),(WIDTH,HEIGHT))

def draw(red,yellow,rb,yb,rh,yh):
   
    WIN.blit(SPACE_IMAGE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    WIN.blit(RED_SPACESHIP,(red.x,red.y ))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y ))
    red_health_text=HEALTH_FONT.render("Health:" + str(rh),1,WHITE)
    yellow_health_text=HEALTH_FONT.render("Health:" + str(yh),1,WHITE)
    WIN.blit(yellow_health_text,(10,10))
    WIN.blit(red_health_text,(WIDTH- red_health_text.get_width()-10,10))
    for bullet in rb :
        pygame.draw.rect(WIN,RED,bullet)
        
    for bullet in yb :
        pygame.draw.rect(WIN,YELLOW,bullet)
        
    pygame.display.update()


def yellow_move(key_pressed,color):
    if key_pressed[pygame.K_q] and color.x-VELOCITY>0:
        color.x-=VELOCITY
    if key_pressed[pygame.K_z] and color.y-VELOCITY>0:
        color.y-=VELOCITY
    if key_pressed[pygame.K_d] and color.x+VELOCITY<445-55:
        color.x+=VELOCITY
    if key_pressed[pygame.K_s]and color.y+VELOCITY<500-40:
        color.y+=VELOCITY
        
def red_move(key_pressed,color):
    if key_pressed[pygame.K_LEFT] and color.x-VELOCITY>465:
        color.x-=VELOCITY
    if key_pressed[pygame.K_UP] and color.y-VELOCITY>0:
        color.y-=VELOCITY
    if key_pressed[pygame.K_RIGHT] and color.x-VELOCITY<900-55:
        color.x+=VELOCITY
    if key_pressed[pygame.K_DOWN] and color.y+VELOCITY<500-40:
        color.y+=VELOCITY


def handle_bullets(yb,rb,y,r):
    for bullet in yb :
        bullet.x+=7
        if r.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yb.remove(bullet)
        
        if bullet.x>900:
            yb.remove(bullet)
            
    for bullet in rb :
        bullet.x-=7
        if y.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            rb.remove(bullet)
            
        if bullet.x<0:
            rb.remove(bullet)
        
      


def draw_winner(text):
    draw_text=WINNER_FONT.render(text,1,WHITE)
    w=draw_text.get_width()+0
    h=draw_text.get_height()+0
    WIN.blit(draw_text,((WIDTH-w)/2
                        ,(HEIGHT-h)/2))
    pygame.display.update()
    pygame.time.delay(5000)
    
        
         
            
            

def main():
    red=pygame.Rect(800,200,55,40)
    yellow=pygame.Rect(100,200,55,40)
    clock=pygame.time.Clock()
    red_bullets=[]
    yellow_bullets=[]
    red_health=10
    yellow_health=10
    
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                run=False
                pygame.quit()
                
                
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(yellow.x + yellow.width,yellow.y + yellow.height//2-2,8,4)
                    yellow_bullets.append(bullet)
                
                if event.key == pygame.K_RCTRL and len(red_bullets)<MAX_BULLETS:
                    bullet=pygame.Rect(red.x ,red.y + red.height//2-2,8,4)
                    red_bullets.append(bullet)
            
            
            if event.type == RED_HIT :
                red_health-=1
                
            if event.type == YELLOW_HIT :
                yellow_health-=1 
            
        winner_text=""
        if red_health <= 0 :
            winner_text="yellow wins!!"  
            
        if yellow_health<= 0 :
            winner_text="red wins!!"
        
        if winner_text != "":
            draw_winner(winner_text)  
            break
                 
                    
        draw(red, yellow,red_bullets,yellow_bullets,red_health,yellow_health)
        
        key_pressed=pygame.key.get_pressed()
        yellow_move(key_pressed,yellow)
        red_move(key_pressed,red)
        
        handle_bullets(yellow_bullets,red_bullets,yellow,red)
        
        
        
    main()
    

if __name__=="__main__":
    main() 