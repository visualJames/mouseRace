import pygame
from enum import Enum

class Direction(Enum):
    No_direction = 0
    Death = 1
    Jump = 2
    Up = 3
    Down = 4
    Left = 5
    Right = 6
    Up_Left = 7
    Up_Right = 8
    Down_Left = 9
    Down_Right = 10



class Player:
    name="Player"
    posX = 420
    posY = 420
    images=None
    leben=3
    endurance= 10
    whichImage=0
    whichImageExactly=0
    def __init__(self, name, posX, posY, images, leben, endurance):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.images = images
        self.leben = leben
        self.endurance = endurance
    def loseLive(self):
        self.leben=self.leben-1
        if(self.leben<=0):
            self.whichImage=Direction.Death
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
                self.whichImage = Direction.Down_Right
            else:
                if (coordinateY <= 0):
                    self.whichImage = Direction.Up_Right
                else:
                    self.whichImage = Direction.Right
        else:
            if (coordinateX <= 0):
                if (coordinateY >= 0):
                    self.whichImage = Direction.Down_Left
                else:
                    if (coordinateY <= 0):
                        self.whichImage = Direction.Up_Left
                    else:
                        self.whichImage = Direction.Left
            else:
                if (coordinateY > 0):
                    self.whichImage = Direction.Up
                else:
                    if(coordinateY < 0):
                        self.whichImage = Direction.Down
                    else:
                        self.whichImage = Direction.No_direction
    def goTo(self, coordinateX, coordinateY):
        self.posX = self.posX+coordinateX
        self.posY = self.posY+coordinateY
        self.change_image(coordinateX,coordinateY)
        self.whichImageExactly +=1
        if(self.whichImageExactly>=len(self.images[self.whichImage.value])):
            self.whichImageExactly = 0
    def draw(self, screen):
        screen.blit(self.images[self.whichImage.value][self.whichImageExactly], (self.posX, self.posY))

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
    down1 = pygame.image.load("mouseplayer/mouseplayer_Down.png")
    down2 = pygame.image.load("mouseplayer/mouseplayer2_Down.png")
    left1 = pygame.image.load("mouseplayer/mouseplayer_Left.png")
    left2 = pygame.image.load("mouseplayer/mouseplayer2_Left.png")
    right1 = pygame.image.load("mouseplayer/mouseplayer_Right.png")
    right2 = pygame.image.load("mouseplayer/mouseplayer2_Right.png")
    up_left1 = pygame.image.load("mouseplayer/mouseplayer_Up_Left.png")
    up_left2 = pygame.image.load("mouseplayer/mouseplayer2_Up_Left.png")
    up_right1 = pygame.image.load("mouseplayer/mouseplayer_Up_Right.png")
    up_right2 = pygame.image.load("mouseplayer/mouseplayer2_Up_Right.png")
    down_right1 = pygame.image.load("mouseplayer/mouseplayer_Down_Right.png")
    down_right2 = pygame.image.load("mouseplayer/mouseplayer2_Down_Right.png")
    down_left1 = pygame.image.load("mouseplayer/mouseplayer_Down_Left.png")
    down_left2 = pygame.image.load("mouseplayer/mouseplayer2_Down_Left.png")
    death = pygame.image.load("mouseplayer/mouseplayerDeath_Up.png")
    return [[right1], [death], [up_right1, up_right2], [up1, up2],
            [down1, down2], [left1, left2], [right1, right2],
            [up_left1, up_left2], [up_right1, up_right2],
            [down_left1, down_left2], [down_right1, down_right2]]
pygame.init()
screen = pygame.display.set_mode((1800,1000))
pygame.display.set_caption("Mouse Race")
mouseheadImage = pygame.image.load('mousehead/mousehead.png')
pygame.display.set_icon(mouseheadImage)

mousePlayerList = [Player("Maus1", 420, 480, load_images(), 3, 5)]
running_loop(screen, mousePlayerList)


