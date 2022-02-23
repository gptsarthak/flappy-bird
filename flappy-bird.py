import pygame
from pygame.locals import *
import random
import sys 

#SETTING UP PYGAME
pygame.init()
screen = pygame.display.set_mode((350,622))
pygame.display.set_caption("Flappy Bird")
bird_flap = pygame.USEREVENT
pygame.time.set_timer(bird_flap, 200)
clock = pygame.time.Clock()
create = pygame.USEREVENT+1
pygame.time.set_timer(create,1200)

#ALL IMPORTS
bg_img = pygame.image.load("source/background.png").convert_alpha()
fl_img = pygame.image.load("source/base.png").convert_alpha()
up = pygame.image.load("source/upflap.png").convert_alpha()
mid = pygame.image.load("source/midflap.png").convert_alpha()
down = pygame.image.load("source/downflap.png").convert_alpha()
pipe_img = pygame.image.load("source/pipe.png").convert_alpha()
game_over_image = pygame.image.load("source/menu.png").convert_alpha()

score_font = pygame.font.Font("source/font.ttf",30)
score_sound = pygame.mixer.Sound("source/point.wav")
flap_sound = pygame.mixer.Sound("source/flap.wav")
fall_sound = pygame.mixer.Sound("source/over.wav")
hit_sound = pygame.mixer.Sound("source/hit.wav")
tophit_sound = pygame.mixer.Sound("source/tophit.wav")


#ALL GLOBAL VARIABLES
index = 0
fl_x = 0
movement = 0
gravity = 0.12
game_over = False
score = 0
high_score = 0

score_time = True
p_height = [300,350,400,533,490]
pipes = []
birds = [up,mid,down]


bird_img = birds[index]
game_over_rect = game_over_image.get_rect(center = (175,331))
bird_rect = bird_img.get_rect(center = (67, 622//2))


#ALL FUNCTIONS
def pipe_animation():
    global game_over, score_time
    for p in pipes:
        if p.top < 0:
            flipped = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped, p)
        else:   
            screen.blit(pipe_img,p)
        p.centerx -= 3
        if p.right < 0:
            pipes.remove(p)

        if bird_rect.colliderect(p):
            game_over = True
            hit_sound.play()

def floor():
    screen.blit(fl_img,(fl_x,550))
    screen.blit(fl_img,(fl_x+448, 550))

def pipe():
    p_y = random.choice(p_height)
    top = pipe_img.get_rect(midbottom = (467, p_y - 215))
    bottom = pipe_img.get_rect(midtop = (467, p_y))
    return top,bottom

def draw_score(game_state):
    if game_state == "game_on":
        score_text = score_font.render(str(score), True, (255,255,255))
        score_rect = score_text.get_rect(center = (175,66))
        screen.blit(score_text, score_rect)
    elif game_state == "game_over":
        score_text = score_font.render(f"Score: {score}", True, (255,255,255))
        score_rect = score_text.get_rect(center = (175,66))
        screen.blit(score_text, score_rect)
        high_score_text = score_font.render(f"High Score: {high_score}", True, (255,255,255))
        high_score_rect = high_score_text.get_rect(center = (175,526))
        screen.blit(high_score_text, high_score_rect)
            
def score_update():
    global score, score_time, high_score
    if pipes:
        for p in pipes:
            if 65 < p.centerx < 70 and score_time:
                score = score + 1
                score_sound.play()
                score_time = False
            if p.left <= 0:
                score_time = True
    high_score = max(score, high_score)


#MAIN LOOP
while True:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE and not game_over:
                movement =  -5
                flap_sound.play()

            if event.key == K_SPACE and game_over:
                game_over = False
                pipes = []
                movement = 0
                bird_rect = bird_img.get_rect(center = (67, 622//2)) 
                score_time = True
                score = 0
                
        if event.type == bird_flap:
            index += 1
            if index > 2:
                index =0

            bird_img = birds[index] 
            bird_rect = bird_img.get_rect(center = bird_rect.center)

        if event.type == create:
            pipes.extend(pipe())

    screen.blit(bg_img,(0,0))
    
    if not game_over:
        movement = movement + gravity
        bird_rect.centery += movement
        rotate = pygame.transform.rotozoom(bird_img,movement*-5,1)

        if bird_rect.top < 5:
            bird_rect = bird_img.get_rect(center =(67, 20)) 
            movement = 1
            score = score - 1
            tophit_sound.play()
            
        if bird_rect.bottom >= 550:
            game_over = True
            fall_sound.play()
            
        screen.blit(rotate, bird_rect)
        pipe_animation()
        score_update()
        draw_score("game_on")
        
    elif game_over:
        screen.blit(game_over_image,game_over_rect)
        draw_score("game_over")
        
    fl_x = fl_x -1
    if fl_x < -448:
        fl_x=0
        
    floor()      
    pygame.display.update()
