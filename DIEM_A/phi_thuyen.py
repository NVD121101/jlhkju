from ast import Str
from re import I
from turtle import width
import pygame
import random
from random import randint
from pygame.locals import *
import button
WIDTH=600
HEIGHT=800
pygame.init()
pygame.display.set_caption("Phi thuyền")
screen = pygame.display.set_mode((WIDTH,HEIGHT))
#load button giao diện
start_img = pygame.image.load('D:/Game_android/DIEM_A/assets/start_btn.png')
exit_img = pygame.image.load('D:/Game_android/DIEM_A/assets/exit_btn.png')

#load hình ảnh, âm thanh, màu sắc
ship = pygame.image.load("D:/Game_android/DIEM_A/phi_thuyen.png")
gem = pygame.image.load("D:/Game_android/DIEM_A/kim_cuong.png")
meto = pygame.image.load("D:/Game_android/DIEM_A/thien_thach.png")
meto2 = pygame.image.load("D:/Game_android/DIEM_A/thien_thach_2.png")
background = pygame.image.load("D:/Game_android/DIEM_A/background.jpg")
font = pygame.font.SysFont('comicsans',30)
font1 = pygame.font.SysFont('comicsans',50)
sound = pygame.mixer.Sound('D:/Game_android/DIEM_A/Explosion2 (1).wav')
sound2 = pygame.mixer.Sound('D:/Game_android/DIEM_A/tick (1).wav')
# Khai bao cac bien
RED = (255,0,0)
FPS=250
speed=2
score = 0
level = 1
gameactive = False
gamewin= False
left,right= False,False
running = True
clock = pygame.time.Clock()
game_over=False
#rect
ship_rect = ship.get_rect(center=(300,750))
gem_rect = gem.get_rect(topleft = (290,0))
meto_rect = meto.get_rect(topleft = (400,0))
meto2_rect = meto2.get_rect(topleft = (150,0))

class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		self.image = img
		self.scale = scale
		self.image = pygame.transform.scale(self.image, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		win.blit(self.image, self.rect)
		return action


def move_ship(left,right):
    if left:
        ship_rect.centerx -= speed
        if ship_rect.left <= 0:
            ship_rect.left = 0
    if right:
        ship_rect.centerx += speed
        if ship_rect.right >= 600:
            ship_rect.right = 600

def move_metro():
    global score,gamewin
    gem_rect.y = gem_rect.y + 2 + score/15
    meto_rect.y = meto_rect.y + 2 + score/15
    meto2_rect.y = meto2_rect.y + 2 + score/15
    if gem_rect.y > 900:
        gem_rect.y = 0
    if meto_rect.y > 900:
        meto_rect.x=randint(20,580)
        meto_rect.y = 0
    if meto2_rect.y > 900:
        meto2_rect.x=randint(20,580)
        meto2_rect.y = -50

def colliderect():
    global score, gameactive, gamewin,level,game_over
    if gem_rect.colliderect(ship_rect):
        gem_rect.x=randint(20,580)
        gem_rect.y = 0
        score += 1
        if ((score+1)%10==1):
            level+=1
        if(score==30):
            gamewin=True
        pygame.mixer.Sound.play(sound2)
    if meto_rect.colliderect(ship_rect):
        gameactive = False
        pygame.mixer.Sound.play(sound)
        game_over = True
        level=1
    if meto2_rect.colliderect(ship_rect):
        gameactive = False
        pygame.mixer.Sound.play(sound)
        game_over = True
        level=1  
def draw():
    screen.blit(background,(0,0))
    screen.blit(ship,ship_rect)
    screen.blit(gem,gem_rect)
    screen.blit(meto,meto_rect)
    screen.blit(meto2,meto2_rect)
    
start_btn = Button(start_img, (150, 100), WIDTH//2-70, HEIGHT//2-100)
exit_btn = Button(exit_img, (120, 100), WIDTH//2-55, HEIGHT//2 + 20)
while running:
    clock.tick(FPS)
    # screen.blit(background,(0,0))
    screen.fill((32, 32, 32))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if gameactive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    left = True
                if event.key == pygame.K_RIGHT:    
                    right = True    
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    left = False
                if event.key == pygame.K_RIGHT:    
                    right = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameactive = True
                gem_rect.y = 0
                meto_rect.y = 0
                meto2_rect.y = 0
                score = 0
                ship_rect = ship.get_rect(center=(300,750))
    if start_btn.draw(screen):
        gameactive = True
    if exit_btn.draw(screen):
        running = False
    if gamewin:
        screen.blit(background,(0,0))
        game_win = font1.render('You Won!',True,RED) 
        screen.blit(game_win,(200,400))
    elif gameactive:
        draw()
        move_metro()
        colliderect()
        move_ship(left,right)
        score_txt = font.render('Score:'+str(score),True,RED)
        level_txt =  font.render('Level:'+str(level),True,RED)
        screen.blit(level_txt,(480,10))
        screen.blit(score_txt,(10,10))
    elif game_over:
        screen.blit(background,(0,0))
        game_over = font1.render('Finally Score:'+str(score),True,RED) 
        screen.blit(game_over,(150,300))
        game_direct = font1.render('Press Space to Start',True,RED) 
        screen.blit(game_direct,(80,400))
    pygame.display.update()

pygame.quit()