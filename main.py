import pygame
from sys import exit
from cowboy import Cowboy
from train import Train
width,height = 900,600
players = 5
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
bg_surface = pygame.image.load("./Assets/desert.png").convert()
bg_surface = pygame.transform.scale(bg_surface,(width,height))
bois = []
posX,posY = 20,490
xd,yd = 160,0
for i in range(players):
    posX += xd
    posY += yd
    bois.append(Cowboy(posX,posY,flip=True))
t1 = Train(nWagons=players)
msCount = 0
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == 768:
            pygame.quit()
            exit()

    if msCount == 500:
        bois[1].flip()
    screen.blit(bg_surface,(0,0))
    t1.idle_animate(screen)
    for i in range(len(bois)):
        bois[i].idle_animate(screen,msCount)
    pygame.display.update()
    msCount +=1
    msCount %= 10000
    clock.tick(60)