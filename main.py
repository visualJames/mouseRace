import pygame
def quit_sequence(quit):
    quit = True
    print("quit")
    return quit

def running_loop(screen):
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit = quit_sequence(quit)
    screen.fill((256,0,0))
    pygame.display.update()

pygame.init()
screen = pygame.display.set_mode((1800,1000))
pygame.display.set_caption("Mouse Race")
mouseheadImage = pygame.image.load('mousehead/mousehead.png')
pygame.display.set_icon(mouseheadImage)
running_loop(screen)



