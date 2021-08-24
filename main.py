import pygame
from enum import Enum

class Direction(Enum):
    Up = 0
    Down = 180
    Left = 270
    Right = 90
    Up_Left = 315
    Up_Right = 45
    Down_Left = 225
    Down_Right = 135
    def get_diff(self, direction):
        return direction.value-self.value


class Player:
    name="Player"
    posX = 420
    posY = 420
    images=None
    leben=3
    endurance= 10
    whichImageDirection=Direction
    whichImageExactly=0
    def __init__(self, name, posX, posY, images, leben, endurance):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.images = images
        self.leben = leben
        self.endurance = endurance
        self.whichImageDirection=Direction.Right

    def set_direction(self, direction):
        angle = self.whichImageDirection.get_diff(direction)
        self.whichImageDirection = direction
        for i in range(0,len(self.images)):
            self.images[i] = pygame.transform.rotate(self.images[i], angle)
    def loseLive(self):
        self.leben=self.leben-1
        if(self.leben<=0):
            #death
            print("death")
    def loseendurance(self):
        if self.endurance>0:
            self.endurance = self.endurance - 1
            return True
        else:
            return False
    def gainLive(self):
        self.leben = self.leben + 1
    def gainendurance(self):
        self.endurance = self.endurance + 1
    def change_image(self, coordinateX, coordinateY):
        if (coordinateX >= 0):
            if (coordinateY >= 0):
                self.set_direction(Direction.Down_Right)
            else:
                if (coordinateY <= 0):
                    self.set_direction(Direction.Up_Right)
                else:
                    self.set_direction(Direction.Right)
        else:
            if (coordinateX <= 0):
                if (coordinateY >= 0):
                    self.set_direction(Direction.Down_Left)
                else:
                    if (coordinateY <= 0):
                        self.set_direction(Direction.Up_Left)
                    else:
                        self.set_direction(Direction.Left)
            else:
                if (coordinateY > 0):
                    self.set_direction(Direction.Up)
                else:
                    if(coordinateY < 0):
                        self.set_direction(Direction.Down)
                    else:
                        self.set_direction(Direction.Right)
        print(self.whichImageDirection)
    def goTo(self, coordinateX, coordinateY):
        self.posX = self.posX+coordinateX
        self.posY = self.posY+coordinateY
        self.change_image(coordinateX,coordinateY)
        self.whichImageExactly +=1
        if(self.whichImageExactly>=len(self.images)):
            self.whichImageExactly = 0
    def draw(self, screen):
        screen.blit(self.images[self.whichImageExactly], (self.posX, self.posY))
    #try it with this logic and it will work better and rotate automatically

def quit_sequence(quit):
    quit = True
    print("quit")
    return quit

def running_loop(screen, mPL):
    quit = False
    mousePlayerList = mPL
    movement = 2
    # RGB- RED, Green, Blue
    while not quit:
        for mouse in mousePlayerList:
            print("vor: ",mouse.posX, mouse.posY, mouse.name, mouse.endurance)
        screen.fill((128, 50, 0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit = quit_sequence(quit)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            print("Enter")
            for mouse in mousePlayerList:
                if mouse.loseendurance():
                    mouse.goTo(movement,-movement)
        if keys[pygame.K_LEFT]:
            print("Left")
            [mouse.goTo(-movement, 0) for mouse in mousePlayerList]
        if keys[pygame.K_RIGHT]:
            print("Right")
            for mouse in mousePlayerList:
                mouse.goTo(movement, 0)
        if keys[pygame.K_UP]:
            print("Up")
            [mouse.goTo(0, -movement) for mouse in mousePlayerList]
        if keys[pygame.K_DOWN]:
            print("Down")
            for mouse in mousePlayerList:
                mouse.goTo(0, movement)
        for mouse in mousePlayerList:
            mouse.draw(screen)
            mouse.gainendurance()
            print("nach: ", mouse.posX, mouse.posY, mouse.name, mouse.endurance)
        pygame.display.update()

def load_images():
    up1 = pygame.image.load("mouseplayer/mouseplayer_Up.png")
    up2 = pygame.image.load("mouseplayer/mouseplayer2_Up.png")
    death = pygame.image.load("mouseplayer/mouseplayerDeath_Up.png")
    return [up1, up2]
pygame.init()
screen = pygame.display.set_mode((1800,1000))
pygame.display.set_caption("Mouse Race")
mouseheadImage = pygame.image.load('mousehead/mousehead.png')
pygame.display.set_icon(mouseheadImage)

mousePlayerList = [Player("Maus1", 420, 480, load_images(), 3, 5)]
running_loop(screen, mousePlayerList)


