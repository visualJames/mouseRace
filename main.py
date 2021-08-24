import pygame
from enum import Enum

class Direction(Enum):
    Up = 0
    Up_Left = 45
    Left = 90
    Down_Left = 135
    Down = 180
    Down_Right = 225
    Right = 270
    Up_Right = 315


    def get_diff(self, direction):
        if(self.value>direction.value):
            return self.value-direction.value
        else:
            return -(direction.value-self.value)
class Team:
    red=0
    blue=1
def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()

    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

    return image
def hexToColour( hash_colour ):
    """Convert a HTML-hexadecimal colour string to an RGB triple-tuple"""
    red   = int( hash_colour[1:3], 16 )
    green = int( hash_colour[3:5], 16 )
    blue  = int( hash_colour[5:7], 16 )
    return ( red, green, blue )

class Player:
    name="Player"
    posX = 420
    posY = 420
    images=None
    leben=3
    endurance= 10
    whichImageDirection=Direction
    whichImageExactly=0
    team=Team.red
    def __init__(self, name, posX, posY, images, leben, endurance, team):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.images = images
        self.leben = leben
        self.endurance = endurance
        self.whichImageDirection=Direction.Right
        self.team = team
    def set_direction(self, direction):
        angle = self.whichImageDirection.get_diff(direction)
        print(angle, direction)
        self.whichImageDirection = direction
        #for i in range(0,len(self.images)):
        #    self.images[i] = pygame.transform.rotate(self.images[i], angle)
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
        if (coordinateX > 0):
            if (coordinateY > 0):
                self.set_direction(Direction.Down_Right)
            else:
                if (coordinateY < 0):
                    self.set_direction(Direction.Up_Right)
                else:
                    self.set_direction(Direction.Right)
        else:
            if (coordinateX < 0):
                if (coordinateY > 0):
                    self.set_direction(Direction.Down_Left)
                else:
                    if (coordinateY < 0):
                        self.set_direction(Direction.Up_Left)
                    else:
                        self.set_direction(Direction.Left)
            else:
                if (coordinateY < 0):
                    print("upDirection:", coordinateX, coordinateY)
                    self.set_direction(Direction.Up)
                else:
                    if(coordinateY > 0):
                        print("downDirection", coordinateX, coordinateY)
                        self.set_direction(Direction.Down)
                    #else:
                     #   self.set_direction(Direction.Right)
        print(self.whichImageDirection)
    def goTo(self, coordinateX, coordinateY):
        self.posX = self.posX+coordinateX
        self.posY = self.posY+coordinateY
        print("coordinates:", coordinateX, " , ", coordinateY)
        self.change_image(coordinateX,coordinateY)
        if(coordinateX!=0 or coordinateY!=0):
            self.whichImageExactly +=1
            if(self.whichImageExactly>=len(self.images)):
                self.whichImageExactly = 0
    def getColor(self):
        if(self.team==Team.red):
            return '#4169E1' #'#0000FF'
        if (self.team == Team.blue):
            return '#FF0000'#'#A52A2A'
        return '#000000'
    def draw(self, screen):
        image = pygame.transform.rotate(self.images[self.whichImageExactly], self.whichImageDirection.value)
        imageBackground = pygame.transform.rotate(pygame.transform.scale(colorize(
            self.images[self.whichImageExactly], hexToColour(self.getColor()))
                                                 , (102,102)), self.whichImageDirection.value)
        screen.blit(imageBackground, (self.posX, self.posY))
        screen.blit(image, (self.posX, self.posY))
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
        coordinateX = [0,0]
        coordinateY = [0,0]
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
                    print("special")
        if keys[pygame.K_LEFT]:
            print("Left")
            coordinateX[Team.red]-=movement
        if keys[pygame.K_RIGHT]:
            print("Right")
            coordinateX[Team.red]+=movement
        if keys[pygame.K_UP]:
            print("Up")
            coordinateY[Team.red]-=movement
        if keys[pygame.K_DOWN]:
            print("Down")
            coordinateY[Team.red]+=movement
        if keys[pygame.K_LEFT]:
            print("Left")
            coordinateX[Team.red] -= movement
        if keys[pygame.K_RIGHT]:
            print("Right")
            coordinateX[Team.red] += movement
        if keys[pygame.K_UP]:
            print("Up")
            coordinateY[Team.red] -= movement
        if keys[pygame.K_DOWN]:
            print("Down")
            coordinateY[Team.red] += movement
        if keys[pygame.K_a]:
            print("a")
            coordinateX[Team.blue] -= movement
        if keys[pygame.K_d]:
            print("d")
            coordinateX[Team.blue] += movement
        if keys[pygame.K_w]:
            print("w")
            coordinateY[Team.blue] -= movement
        if keys[pygame.K_s]:
            print("s")
            coordinateY[Team.blue] += movement
        for mouse in mousePlayerList:
            mouse.goTo(coordinateX[mouse.team], coordinateY[mouse.team])
            mouse.draw(screen)
            mouse.gainendurance()
            print("nach: ", mouse.posX, mouse.posY, mouse.name, mouse.endurance)
        pygame.display.update()

def load_images():
    up1 = pygame.image.load("mouseplayer/mouseplayer_Up.png")
    up2 = pygame.image.load("mouseplayer/mouseplayer2_Up.png")
    up3 = pygame.image.load("mouseplayer/mouseplayer3_Up.png")
    up4 = pygame.image.load("mouseplayer/mouseplayer4_Up.png")
    death = pygame.image.load("mouseplayer/mouseplayerDeath_Up.png")
    return [up1, up4, up3, up2, up3, up4]
pygame.init()
screen = pygame.display.set_mode((1800,1000))
pygame.display.set_caption("Mouse Race")
mouseheadImage = pygame.image.load('mousehead/mousehead.png')
pygame.display.set_icon(mouseheadImage)

mousePlayerList = [Player("Maus1", 120, 80, load_images(), 3, 5, Team.red),Player("Maus1", 120, 180, load_images(), 3, 5, Team.red),
                    Player("Maus1", 120, 280, load_images(), 3, 5, Team.red),Player("Maus1", 120, 380, load_images(), 3, 5, Team.red),
                   Player("Maus1", 120, 480, load_images(), 3, 5, Team.blue),Player("Maus1", 120, 580, load_images(), 3, 5, Team.blue),
                   Player("Maus1", 120, 680, load_images(), 3, 5, Team.blue),Player("Maus1", 120, 780, load_images(), 3, 5, Team.blue)]
running_loop(screen, mousePlayerList)


