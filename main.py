import random

import pygame
from enum import Enum
import numpy


def get_diff(this, other):
    if (this > other):
        return this - other
    else:
        return -(other - this)

class Hive_Direction(Enum):
    Nothing = 0
    Merge = 1
    Diverge = 2

class Direction(Enum):
    Up = 0
    Up_Left = 45
    Left = 90
    Down_Left = 135
    Down = 180
    Down_Right = 225
    Right = 270
    Up_Right = 315

    def opposite(self):
        if self==Direction.Up:
            return Direction.Down
        if self==Direction.Up_Left:
            return Direction.Down_Right
        if self==Direction.Left:
            return Direction.Right
        if self==Direction.Down_Left:
            return Direction.Up_Right
        if self==Direction.Down:
            return Direction.Up
        if self==Direction.Down_Right:
            return Direction.Up_Left
        if self==Direction.Right:
            return Direction.Left
        if self==Direction.Up_Right:
            return Direction.Down_Left

    def move(self, movement):
        if self==Direction.Up:
            return (0,-movement)
        if self==Direction.Up_Left:
            return (-movement,-movement)
        if self==Direction.Left:
            return (-movement,0)
        if self==Direction.Down_Left:
            return (-movement,movement)
        if self==Direction.Down:
            return (0,movement)
        if self==Direction.Down_Right:
            return (movement,movement)
        if self==Direction.Right:
            return (movement,0)
        if self==Direction.Up_Right:
            return (movement,-movement)


    def get_diff(self, direction):
        get_diff(self.value, direction.value)
    def average(list):
        coordinateX=0
        coordinateY=0
        for mouse in list:
            coordinateX+=mouse.posX
            coordinateY+=mouse.posY
        length = len(list)
        return (coordinateX//length, coordinateY//length)
    def aboveOrUnder(this:(int,int), other:(int,int)):
        (thisX, thisY) = this
        (otherX, otherY) = other
        diffX = -get_diff(thisX, otherX)
        diffY = -get_diff(thisY, otherY)
        print(otherY, "=",thisY ,"+ (",diffY, ")")
        return Direction.aboveOrUnderDiff(diffX, diffY)
    def aboveOrUnderDiff(coordinateX:int, coordinateY:int):
        if (coordinateX > 0):
            if (coordinateY > 0):
                return Direction.Down_Right
            else:
                if (coordinateY < 0):
                    return Direction.Up_Right
                else:
                    return Direction.Right
        else:
            if (coordinateX < 0):
                if (coordinateY > 0):
                    return Direction.Down_Left
                else:
                    if (coordinateY < 0):
                        return Direction.Up_Left
                    else:
                        return Direction.Left
            else:
                if (coordinateY < 0):
                    print("upDirection:", coordinateX, coordinateY)
                    return Direction.Up
                else:
                    if (coordinateY > 0):
                        print("downDirection", coordinateX, coordinateY)
                        return Direction.Down
                    else: print("None in aboveOrUnder")

class Team:
    Red=0
    Blue=1
    No_team=2
    def getTeam(team, list):
        l = []
        for mouse in list:
            if mouse.team==team:
                l.append(mouse)
        return l
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



class Color(Enum):
    Blue= '#4169E1'
    Red= '#FF0000'
    Black= '#000000'
    Grey= '#787878'

def getNameAsImage(name, font_size, color=Color.Grey):
    font = pygame.font.SysFont(None, font_size)
    return font.render(name, True, hexToColour(color.value))

class Player:
    whichImageExactly=0
    def __init__(self, name, posX, posY, images, live, endurance, team):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.images = images
        self.live = live-1
        self.max_life = live
        self.endurance = endurance-1
        self.max_endurance = endurance
        self.whichImageDirection=Direction.Right
        self.team = team
    def set_direction(self, direction: 'Direction'):
        angle = self.whichImageDirection.get_diff(direction)
        print(angle, direction)
        self.whichImageDirection = direction
        #for i in range(0,len(self.images)):
        #    self.images[i] = pygame.transform.rotate(self.images[i], angle)
    def loseLive(self):
        self.live=self.live-1
        if(self.live<=0):
            #death
            print("death")
    def loseendurance(self):
        if self.endurance>0:
            self.endurance = self.endurance - 1
            return True
        else:
            return False
    def gainLive(self):
        if self.live < self.max_life:
            self.live = self.live + 1
    def gainendurance(self):
        if self.endurance < self.max_endurance:
            self.endurance = self.endurance + 1
    def change_image(self, direction: 'Direction'):
        self.set_direction(direction)
        print(self.whichImageDirection)

    def isNearOfDirectionValues(self, posX, posY, range, width, heigth):
        isUp=self.posY < posY + range*heigth
        isDown=self.posY > posY - range*heigth
        isRight = self.posX>posX-range*width
        isLeft = self.posX<posX+range*width
        return (isUp, isDown, isRight, isLeft)
    def isNear(self, range, posX, posY, width, heigth):
        (isUp, isDown, isRight, isLeft) = self.isNearOfDirectionValues(posX, posY, range, width, heigth)
        if(isLeft and isRight):
            if (isUp and isDown):
                return True
        return False
    def isNearOfDirection(self, direction, posX, posY, range, width, heigth):
        (isUp, isDown, isRight, isLeft) = self.isNearOfDirectionValues(posX, posY, range, width, heigth)
        if direction==Direction.Up:
            return isUp
        if direction==Direction.Up_Left:
            return  isUp or isLeft
        if direction==Direction.Left:
            return isLeft
        if direction==Direction.Down_Left:
            return isDown or isLeft
        if direction==Direction.Down:
            return isDown
        if direction==Direction.Down_Right:
            return isDown or isRight
        if direction==Direction.Right:
            return isRight
        if direction==Direction.Up_Right:
            return isUp or isRight

    def goTo(self, coordinateX, coordinateY, game, hive_direction):
        movement = 2
        howNear=50
        healing_distance = 1.75
        width = 0.8
        heigth = 0.8
        direction = Direction.aboveOrUnderDiff(coordinateX, coordinateY)
        for mouse in game.mPL:
            if (self != mouse and mouse.isNear(howNear*healing_distance, self.posX + coordinateX, self.posY + coordinateY, width, heigth)):
                if numpy.random.random_sample()<=0.01:
                    mouse.gainLive() #heal other mouse (every mouse even of enemy team)
                if mouse.team==Team.No_team:
                    mouse.team=self.team #(neutral mouse joins team)
                if(mouse.isNear(howNear, self.posX+coordinateX, self.posY+coordinateY, width, heigth)):
                    if(mouse.isNearOfDirection(direction, self.posX+coordinateX, self.posY+coordinateY, movement, width, heigth)):
                        return #someone else is standing there
        if direction != None:
            self.change_image(direction)
            if(coordinateX!=0 or coordinateY!=0):
                self.whichImageExactly +=1
                if(self.whichImageExactly>=len(self.images)):
                    self.whichImageExactly = 0

            (x, y) = direction.move(movement)
            self.posX += x
            self.posY += y
    def getColor(self):
        if(self.team==Team.Blue):
            return Color.Blue.value
        if (self.team == Team.Red):
            return Color.Red.value
        return Color.Black.value
    def draw(self, screen):
        image = pygame.transform.rotate(self.images[self.whichImageExactly], self.whichImageDirection.value)
        imageBackground = pygame.transform.rotate(pygame.transform.scale(colorize(
            self.images[self.whichImageExactly], hexToColour(self.getColor()))
                                                 , (102,102)), self.whichImageDirection.value)
        screen.blit(imageBackground, (self.posX, self.posY))
        screen.blit(image, (self.posX, self.posY))
        font_size = 21
        screen.blit(getNameAsImage(self.name, font_size),(self.posX+25, self.posY+85))

    def draw_Minimap(self, screen, size, posX_map, posY_map):
        image = pygame.transform.scale(pygame.transform.rotate(self.images[self.whichImageExactly], self.whichImageDirection.value),(size,size))
        imageBackground = pygame.transform.scale(pygame.transform.rotate(pygame.transform.scale(colorize(
            self.images[self.whichImageExactly], hexToColour(self.getColor()))
            , (102, 102)), self.whichImageDirection.value),(size,size))
        screen.blit(imageBackground, (posX_map, posY_map))
        screen.blit(image, (posX_map, posY_map))
        font_size = 7
        #screen.blit(getNameAsImage(self.name, font_size), (posX_map + 3, posY_map + 9))
    #try it with this logic and it will work better and rotate automatically

def quit_sequence(quit):
    quit = True
    print("quit")
    return quit

class Minimap(pygame.sprite.Sprite):
    def __init__(self, game, width_view, height_view, size_relation):
        pygame.sprite.Sprite.__init__(self)
        self.width = game.map.width
        self.height = game.map.height
        self.surface = pygame.Surface((round(self.width/size_relation), round(self.height/size_relation)))
        self.surface.fill((0, 0, 0))
        self.game = game
        self.image = self.surface
        self.posX = self.width-width_view/size_relation
        self.posY = 0
        self.size_relation=size_relation
        self.hearth =  pygame.image.load("Hearth/heart.png")
        self.hearth_not_here = pygame.image.load("Hearth/heart_not_here.png")
        self.sweat = pygame.image.load("Sweat/Sweat.png")
        self.sweat_not_here = pygame.image.load("Sweat/Sweat_not_here.png")
    def draw_teams(self, font_size, color, team, name_team, start_posY, step):
        screen.blit(getNameAsImage("Team:", font_size), (self.posX, start_posY))
        screen.blit(getNameAsImage(name_team, font_size, color),
                    (self.posX + 65, start_posY + 2))
        y = 22
        for mouse in team:
            screen.blit(getNameAsImage(mouse.name, font_size),
                        (self.posX + 25, start_posY + y))
            for i in range(0, mouse.live):
                screen.blit(self.hearth,
                            (self.posX + 145 + i * 10, start_posY + y + 5))
            for i in range(mouse.live, mouse.max_life):
                screen.blit(self.hearth_not_here,
                            (self.posX + 145 + i * 10, start_posY + y + 5))
            for i in range(0, mouse.endurance):
                screen.blit(self.sweat,
                            (self.posX + 195 + i * 10, start_posY + y + 5))
            for i in range(mouse.endurance, mouse.max_endurance):
                screen.blit(self.sweat_not_here,
                            (self.posX + 195 + i * 10, start_posY + y + 5))
            screen.blit(getNameAsImage("(" + str(mouse.posX) + "," + str(mouse.posY) + ")", font_size),
                        (self.posX + 235, start_posY + y))
            y += step

    def draw(self, screen):
        self.image = self.surface.copy()
        screen.blit(self.image, (self.posX, self.posY))

        for mouse in self.game.mPL:
            posX = mouse.posX / self.size_relation + self.posX
            posY = mouse.posY / self.size_relation + self.posY
            mouse.draw_Minimap(screen, round(100/self.size_relation), posX, posY)

        step = 20
        font_size = 28
        color = Color.Blue
        team = Team.getTeam(Team.Blue, mousePlayerList)
        name_team = "BLUE"
        start_posY = self.posY + self.height/self.size_relation
        self.draw_teams(font_size, color, team, name_team, start_posY, step)
        color = Color.Red
        team = Team.getTeam(Team.Red, mousePlayerList)
        name_team = "RED"
        start_posY = self.posY + self.height / self.size_relation + (len(team)+3)*step
        self.draw_teams(font_size, color, team, name_team, start_posY, step)



class Camera:
    def __init__(self, posX, posY):
        self.posX = posX
        self.posY = posY
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
class Game:
    def __init__(self, mPL, camera, map):
        self.mPL= mPL
        self.camera=camera
        self.map = map

def running_loop(screen, game):
    quit = False
    movement = 2
    size_relation = 5
    minimap = Minimap(game,game.map.width, game.map.height, size_relation)
    # RGB- RED, Green, Blue
    while not quit:
        coordinateX = [0,0,0]
        coordinateY = [0,0,0]
        for mouse in game.mPL:
            print("vor: ",mouse.posX, mouse.posY, mouse.name, mouse.endurance)
        screen.fill((128, 50, 0))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit = quit_sequence(quit)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            print("Enter")
            for mouse in game.mPL:
                if mouse.loseendurance():
                    print("special")
        if keys[pygame.K_LEFT]:
            print("Left")
            coordinateX[Team.Red]-=movement
        if keys[pygame.K_RIGHT]:
            print("Right")
            coordinateX[Team.Red]+=movement
        if keys[pygame.K_UP]:
            print("Up")
            coordinateY[Team.Red]-=movement
        if keys[pygame.K_DOWN]:
            print("Down")
            coordinateY[Team.Red]+=movement
        hive_direction = [Hive_Direction.Nothing, Hive_Direction.Nothing, Hive_Direction.Nothing]
        if keys[pygame.K_COMMA]:
            print("Comma")
            hive_direction[Team.Red] = Hive_Direction.Diverge
        if keys[pygame.K_MINUS]:
            print("Minus")
            hive_direction[Team.Red] = Hive_Direction.Merge

        if keys[pygame.K_a]:
            print("a")
            coordinateX[Team.Blue] -= movement
        if keys[pygame.K_d]:
            print("d")
            coordinateX[Team.Blue] += movement
        if keys[pygame.K_w]:
            print("w")
            coordinateY[Team.Blue] -= movement
        if keys[pygame.K_s]:
            print("s")
            coordinateY[Team.Blue] += movement
        if keys[pygame.K_q]:
            print("q")
            hive_direction[Team.Blue] = Hive_Direction.Diverge
        if keys[pygame.K_e]:
            print("e")
            hive_direction[Team.Blue] = Hive_Direction.Merge
        for mouse in game.mPL:
            (coordinateX_Hive, coordinateY_Hive) = (0, 0)
            if hive_direction[mouse.team]!=Hive_Direction.Nothing:
                team = Team.getTeam(mouse.team, game.mPL)
                direction = Direction.aboveOrUnder((mouse.posX, mouse.posY), Direction.average(team))
                if direction != None:
                    if hive_direction[mouse.team]==Hive_Direction.Merge:
                        (coordinateX_Hive, coordinateY_Hive) = direction.move(movement)
                    else:#Diverge
                        (coordinateX_Hive, coordinateY_Hive) = direction.opposite().move(movement)

            mouse.goTo(coordinateX[mouse.team]+coordinateX_Hive, coordinateY[mouse.team]+coordinateY_Hive, game, hive_direction)
            mouse.draw(screen)
            if numpy.random.random_sample()<=0.01:
                mouse.gainendurance()
            print("nach: ", mouse.posX, mouse.posY, mouse.name, mouse.endurance)
        minimap.draw(screen)
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
mouseheadImage = pygame.image.load("mouseplayer/mouseplayerDeath_Up.png")#pygame.image.load('mousehead/mousehead.png')
pygame.display.set_icon(mouseheadImage)
nameList = ["Bernd", "Jürgen", "Hanz", "Herbert", "Thomas"]
nameList2 = ["Aaron", "Felix", "Satella", "Torben", "Frank"]
nameList3 = ["Sven", "Max", "Lukas"]
mousePlayerList = []
y=150
team = Team.Red
for name in nameList:
    mousePlayerList.append(Player(name, 120, y, load_images(), 3, 2, team))
    y+=150
team = Team.Blue
y= 75
for name in nameList2:
    mousePlayerList.append(Player(name, 120, y, load_images(), 3, 2, team))
    y += 150
team = Team.No_team
y = 275
for name in nameList3:
    mousePlayerList.append(Player(name, 720, y, load_images(), 3, 2, team))
    y += 150
camera = Camera(0,0)
width = screen.get_width()
height = screen.get_height()
map = Map(width, height)
game = Game(mousePlayerList, camera, map)
running_loop(screen, game)


