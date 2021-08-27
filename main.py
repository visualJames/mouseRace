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
    def getByValue(value):
        if value>335 or value<25:
            return Direction.Up
        elif value<70:
            return Direction.Up_Left
        elif value<115:
            return Direction.Left
        elif value<160:
            return Direction.Down_Left
        elif value<205:
            return Direction.Down
        elif value<250:
            return Direction.Down_Right
        elif value<295:
            return Direction.Right
        else:
            return Direction.Up_Right

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
        return get_diff(self.value, direction.value)
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
    def aboveOrUnderDiff(coordinateX:int, coordinateY:int, buffer=0):
        if (coordinateX-buffer > 0):
            if (coordinateY-buffer > 0):
                return Direction.Down_Right
            else:
                if (coordinateY+buffer < 0):
                    return Direction.Up_Right
                else:
                    return Direction.Right
        else:
            if (coordinateX+buffer < 0):
                if (coordinateY-buffer > 0):
                    return Direction.Down_Left
                else:
                    if (coordinateY+buffer < 0):
                        return Direction.Up_Left
                    else:
                        return Direction.Left
            else:
                if (coordinateY+buffer < 0):
                    return Direction.Up
                else:
                    if (coordinateY-buffer > 0):
                        return Direction.Down
                    else: pass#print("None in aboveOrUnder")

class Team(Enum):
    Red=0
    Blue=1
    No_team=2
    Evil=3
    def getName(self):
        return self.name
    def getColor(self):
        if self==Team.Blue:
            return Color.Blue
        if self==Team.Red:
            return Color.Red
        if self==Team.No_team:
            return Color.Grey
        if self==Team.Evil:
            return Color.Black
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
    Dirt= '#9b7653'
    Violet= '#8A2BE2'

def getNameAsImage(name, font_size, color=Color.Grey, font_type = None):
    font = pygame.font.SysFont(font_type, font_size)
    return font.render(name, True, hexToColour(color.value))

class Snake:
    def __init__(self, name, posX, posY, imagesHead, imagesBody, imagesTail, live, endurance):
        self.Head = Player(name, posX, posY, imagesHead, live, endurance, Team.Evil)
        self.imagesBody = imagesBody
        self.imagesTail = imagesTail
        self.sizeOfBodyParts = 42
        self.Body = []
        self.updateBody()
        self.size_of_shade = (51,51)
        self.movement = 5
    def appendBodyPart(self, before):
        direction = before.whichImageDirection
        b = Player("", before.posX, before.posY, self.imagesBody, 1, 0,
                   Team.Evil)
        b.set_direction(direction)
        self.Body.append(b)
    def updateBody(self):
        lenBody = len(self.Body)
        if lenBody >= self.Head.live+1:
            return
        if lenBody == 0:
            b = Player("", self.Head.posX - self.sizeOfBodyParts, self.Head.posY,
                       self.imagesBody, 1, 0, Team.Evil)
            b.set_direction(self.Head.whichImageDirection)
            # print("Tail:", tail)
            self.Body.append(b)
        else:
            before = self.Body.pop()
            self.appendBodyPart(before)
        for i in range(lenBody+1, self.Head.live):
            self.appendBodyPart(before)
        lastBody = self.Body[len(self.Body)-1]
        tail = Player("", lastBody.posX - self.sizeOfBodyParts, lastBody.posY,
                      self.imagesTail, 1, 0, Team.Evil)
        tail.set_direction(lastBody.whichImageDirection)
        # print("Tail:", tail)
        self.Body.append(tail)
        print(self.Body, "Snake-Body")
    def draw(self,map):
        self.Head.draw(map, self.size_of_shade)
        for b in self.Body:
            b.draw(map,self.size_of_shade)
    def draw_Minimap(self, screen, size, posX_map, posY_map):
        self.Head.draw_Minimap(screen, size, posX_map, posY_map)#Todo:better image for snake-minimap
        #for b in self.Body:
        #    b.draw_Minimap(screen, size, posX_map, posY_map)
    def change_image(self, direction):
        diff = self.Head.whichImageDirection.get_diff(direction)
        print(diff, "change_image", direction, self.Head.whichImageDirection)
        if(diff!=None):
            if abs(diff)>90:
                if diff<0:
                    direction = self.Head.whichImageDirection.value - 90
                    if direction<0:
                        direction+=360
                else:
                    direction = self.Head.whichImageDirection.value + 90
                direction = Direction.getByValue(direction)
            before = self.Body[0].whichImageDirection
            self.Body[0].change_image(self.Head.whichImageDirection)
            self.Head.change_image(direction)
            (x,y)=self.Head.whichImageDirection.move(self.sizeOfBodyParts)
            self.Body[0].posX = self.Head.posX - x
            self.Body[0].posY = self.Head.posY - y
            for i in range(1,len(self.Body)):
                zwischen = self.Body[i].whichImageDirection
                self.Body[i].change_image(before)
                before = zwischen
                (x, y) = self.Body[i].whichImageDirection.move(self.sizeOfBodyParts)
                self.Body[i].posX = self.Body[i-1].posX - x/1.1
                self.Body[i].posY = self.Body[i-1].posY - y/1.1

    def goTo(self, coordinateX, coordinateY, game):
        movement = self.movement
        howNear = 50
        food_distance = 1.15
        width = 0.8
        heigth = 0.8
        direction = Direction.aboveOrUnderDiff(coordinateX, coordinateY, 20)
        if direction != None:
            self.change_image(direction)
            if (coordinateX != 0 or coordinateY != 0):
                self.Head.whichImageExactly += 1 # Todo:later body changes images too
                if (self.Head.whichImageExactly >= len(self.Head.images)):
                    self.Head.whichImageExactly = 0

            (x, y) = direction.move(movement)
            for i in range(0, len(game.mPL)):
                if (game.mPL[i].isNear(howNear * food_distance, self.Head.posX+x,
                                       self.Head.posY+y, width, heigth)):
                    pygame.mixer.music.stop()
                    game.musicPlayer.time_to_wait=30
                    pygame.mixer.Sound("Music/Eat.wav").play()
                    mouse_died = game.mPL.pop(i)
                    print("Mouse died: ", mouse_died.name)
                    self.Head.live += 1
                    self.updateBody()
                    break
            self.Head.posX += x
            self.Head.posY += y
            for b in self.Body:
                b.posX += x
                b.posY += y

class Player:
    whichImageExactly=0
    def __init__(self, name, posX, posY, images, live, endurance, team):
        self.name = name
        self.posX = posX
        self.posY = posY
        self.images = images
        self.live = live-1
        self.max_life = live
        if endurance > 0:
            self.endurance =endurance-1
            self.max_endurance = endurance
        else:
            self.endurance =0
            self.max_endurance = 0
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

    def goTo(self, coordinateX, coordinateY, game):
        movement = 4
        howNear=50
        healing_distance = 1.75
        width = 0.8
        heigth = 0.8
        direction = Direction.aboveOrUnderDiff(coordinateX, coordinateY)
        if direction != None:
            self.change_image(direction)
            if(coordinateX!=0 or coordinateY!=0):
                self.whichImageExactly +=1
                if(self.whichImageExactly>=len(self.images)):
                    self.whichImageExactly = 0

            (x, y) = direction.move(movement)
            for mouse in game.mPL:
                if (self != mouse and mouse.isNear(howNear * healing_distance, self.posX + x,
                                                   self.posY + y, width, heigth)):
                    if numpy.random.random_sample() <= 0.01:
                        mouse.gainLive()  # heal other mouse (every mouse even of enemy team)
                    if mouse.team == Team.No_team:
                        mouse.team = self.team  # (neutral mouse joins team)
                    if (mouse.isNear(howNear, self.posX + x, self.posY + y, width, heigth)):
                        if (
                        mouse.isNearOfDirection(direction, self.posX + x, self.posY + y, movement,
                                                width, heigth)):
                            return  # someone else is standing there
            self.posX += x
            self.posY += y
    def getColor(self):
        if(self.team==Team.Blue):
            return Color.Blue.value
        if (self.team == Team.Red):
            return Color.Red.value
        return Color.Black.value
    def draw(self, map, size_of_shade=(102,102)):
        image = pygame.transform.rotate(self.images[self.whichImageExactly], self.whichImageDirection.value)
        imageBackground = pygame.transform.rotate(pygame.transform.scale(colorize(
            self.images[self.whichImageExactly], hexToColour(self.getColor()))
                                                 ,size_of_shade), self.whichImageDirection.value)
        map.blit(imageBackground, (self.posX, self.posY))
        map.blit(image, (self.posX, self.posY))
        font_size = 21
        map.blit(getNameAsImage(self.name, font_size),(self.posX+25, self.posY+85))

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
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        size_relation = 5
        self.size_relationWidth = game.map.width / game.map.camera.width * size_relation
        self.size_relationHeight = game.map.height / game.map.camera.height * size_relation
        self.width = game.map.width
        self.height = game.map.height
        self.surface = pygame.Surface((round(self.width/self.size_relationWidth),
                                       round(self.height/self.size_relationHeight)))
        self.surface.fill((0, 0, 0))
        self.game = game
        self.image = self.surface
        self.posX = 0
        self.posY = 0
        self.hearth =  pygame.image.load("Hearth/heart.png")
        self.hearth_not_here = pygame.image.load("Hearth/heart_not_here.png")
        self.sweat = pygame.image.load("Sweat/Sweat.png")
        self.sweat_not_here = pygame.image.load("Sweat/Sweat_not_here.png")
    def draw_teams(self, screen, font_size, color, team, name_team, start_posY, step):
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

    def draw(self, map):
        self.image = self.surface.copy()
        map.screen.blit(self.image, (self.posX, self.posY))

        minimap_size = round(100/self.size_relationWidth)
        for mouse in self.game.mPL:
            posX = mouse.posX / self.size_relationWidth + self.posX
            posY = mouse.posY / self.size_relationHeight + self.posY
            mouse.draw_Minimap(map.screen, minimap_size , posX, posY)
        snake = self.game.snake.Head
        posX = snake.posX / self.size_relationWidth + self.posX
        posY = snake.posY / self.size_relationHeight + self.posY
        self.game.snake.draw_Minimap(map.screen, minimap_size , posX, posY)
        step = 20
        font_size = 28
        lenOldTeams=0
        i = 1
        for team in Team:
            start_posY = self.posY + self.height / self.size_relationHeight + (lenOldTeams + i) * step
            color = team.getColor()
            team_list = team.getTeam(self.game.mPL)
            if not team_list:
                continue
            name_team = team.getName()
            self.draw_teams(map.screen, font_size, color, team_list, name_team, start_posY, step)
            lenOldTeams += len(team_list)
            i+=3

class Camera:
    def __init__(self, posX, posY, width, height):
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
    def move(self, posX, posY):
        self.posX=posX
        self.posY=posY

def changeMusicOfTerrain(biom, musicPlayer):
    music = biom.getMusic()
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.queue(music)
    else:
        if musicPlayer.time_to_wait > 0:
            musicPlayer.time_to_wait-= 1
            return
        pygame.mixer.music.load(music)
        pygame.mixer.music.play()
class Map:
    def __init__(self, width, height, screen, camera, terrain):
        self.width = width
        self.height = height
        self.screen = screen
        self.camera = camera
        self.terrain = terrain
    def blit(self, image, pos):
        (posX, posY)=pos
        self.screen.blit(image, (posX-self.camera.posX, posY-self.camera.posY))
    def fill(self, musicPlayer):
        for t in self.terrain:
            if t.isInTerrain(self.camera.posX, self.camera.posY):
                t.fill(self.screen)
                changeMusicOfTerrain(t.biom, musicPlayer)
                return
        self.screen.fill((128, 50, 0))
class MusicPlayer:
    def __init__(self):
        self.time_to_wait = 0
class Game:
    def __init__(self, mPL, snake, map):
        self.mPL= mPL
        self.snake = snake
        self.map = map
        self.musicPlayer = MusicPlayer()
        changeMusicOfTerrain(Biom.No_cave, self.musicPlayer)


def paused(game):
    PauseText = getNameAsImage("Paused", 215, Color.Red, "comicsansms")
    pygame.mixer.music.stop()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return

        game.map.screen.fill(hexToColour(Color.Grey.value))
        game.map.screen.blit(PauseText, ((game.map.camera.width / 2.8), (game.map.camera.height / 2.3)))

#        button("Continue", 150, 450, 100, 50, green, bright_green, unpause)
 #       button("Quit", 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()
        pygame.time.wait(200)

def running_loop(game):
    quit = False
    movement = 2
    minimap = Minimap(game)
    # RGB- RED, Green, Blue
    while not quit:
        camera_pos_X = 2.6
        camera_pos_Y = 2.1
        game.map.camera.move(game.snake.Head.posX-game.map.camera.width/camera_pos_X,
                             game.snake.Head.posY-game.map.camera.height/camera_pos_Y)
        coordinateX = [0,0,0]
        coordinateY = [0,0,0]
        game.map.fill(game.musicPlayer)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                quit = quit_sequence(quit)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            paused(game)
        if keys[pygame.K_RETURN]:
            print("Enter")
            for mouse in game.mPL:
                if mouse.loseendurance():
                    print("special")
        if keys[pygame.K_LEFT]:
            print("Left")
            coordinateX[Team.Red.value]-=movement
        if keys[pygame.K_RIGHT]:
            print("Right")
            coordinateX[Team.Red.value]+=movement
        if keys[pygame.K_UP]:
            print("Up")
            coordinateY[Team.Red.value]-=movement
        if keys[pygame.K_DOWN]:
            print("Down")
            coordinateY[Team.Red.value]+=movement
        hive_direction = [Hive_Direction.Nothing, Hive_Direction.Nothing, Hive_Direction.Nothing]
        if keys[pygame.K_COMMA]:
            print("Comma")
            hive_direction[Team.Red.value] = Hive_Direction.Diverge
        if keys[pygame.K_MINUS]:
            print("Minus")
            hive_direction[Team.Red.value] = Hive_Direction.Merge

        if keys[pygame.K_a]:
            print("a")
            coordinateX[Team.Blue.value] -= movement
        if keys[pygame.K_d]:
            print("d")
            coordinateX[Team.Blue.value] += movement
        if keys[pygame.K_w]:
            print("w")
            coordinateY[Team.Blue.value] -= movement
        if keys[pygame.K_s]:
            print("s")
            coordinateY[Team.Blue.value] += movement
        if keys[pygame.K_q]:
            print("q")
            hive_direction[Team.Blue.value] = Hive_Direction.Diverge
        if keys[pygame.K_e]:
            print("e")
            hive_direction[Team.Blue.value] = Hive_Direction.Merge
        for mouse in game.mPL:
            (coordinateX_Hive, coordinateY_Hive) = (0, 0)
            if hive_direction[mouse.team.value]!=Hive_Direction.Nothing:
                team = mouse.team.getTeam(game.mPL)
                direction = Direction.aboveOrUnder((mouse.posX, mouse.posY), Direction.average(team))
                if direction != None:
                    if hive_direction[mouse.team.value]==Hive_Direction.Merge:
                        (coordinateX_Hive, coordinateY_Hive) = direction.move(movement)
                    else:#Diverge
                        (coordinateX_Hive, coordinateY_Hive) = direction.opposite().move(movement)
            if mouse.team==Team.No_team:
                snake = game.snake.Head
                width = 1.3
                heigth = 1.3
                if mouse.isNear(snake.posX, snake.posY, game.snake.movement, width, heigth):
                    directionSnake = snake.whichImageDirection
                    direction = directionSnake
                    (x,y)=direction.move(game.snake.movement)
                    mouse.goTo(x,y, game)

            mouse.goTo(coordinateX[mouse.team.value]+coordinateX_Hive, coordinateY[mouse.team.value]+coordinateY_Hive, game)
            mouse.draw(game.map)
            if numpy.random.random_sample()<=0.01:
                mouse.gainendurance()
        (snakeDirectionX, snakeDirectionY) = pygame.mouse.get_pos()
        snakeDirectionX -= game.snake.Head.posX
        snakeDirectionY -= game.snake.Head.posY
        game.snake.goTo(snakeDirectionX, snakeDirectionY, game)
        game.snake.draw(game.map)
        minimap.draw(game.map)
        pygame.display.update()
class Biom(Enum):
    No_cave = 0
    Mouse_cave = 1
    Spider_cave = 2
    def getColor(self):
        if self==Biom.No_cave:
            return Color.Grey
        if self==Biom.Mouse_cave:
            return Color.Dirt
        if self==Biom.Spider_cave:
            return Color.Violet
    def getMusic(self):
        if self == Biom.No_cave:
            return "Music/suprised.wav"
        if self == Biom.Mouse_cave:
            return "Music/entuhsiastic.wav"
        if self == Biom.Spider_cave:
            return "Music/dark-atomosphere.wav"
def howDeep(terrain):
    return terrain.posY_end
class Terrain:
    def __init__(self, biom,posY_end):
        self.posY_end=posY_end
        self.biom = biom
    def isInTerrain(self, posX, posY):
        if posY<=self.posY_end:
            return True
        else:
            return False
    def fill(self, screen):
        screen.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
        # add in new RGB values
        c = hexToColour(self.biom.getColor().value)
        screen.fill(c[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)

def load_images():
    up1 = pygame.image.load("mouseplayer/mouseplayer_Up.png")
    up2 = pygame.image.load("mouseplayer/mouseplayer2_Up.png")
    up3 = pygame.image.load("mouseplayer/mouseplayer3_Up.png")
    up4 = pygame.image.load("mouseplayer/mouseplayer4_Up.png")
    death = pygame.image.load("mouseplayer/mouseplayerDeath_Up.png")
    return [up1, up4, up3, up2, up3, up4]
def init():
    pygame.init()
    screen = pygame.display.set_mode((1910,1005))
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
    snakeImageHead = pygame.transform.rotate(pygame.image.load("Snake/SnakeHead.png"), Direction.Left.value)
    snakeImageBody = pygame.transform.rotate(pygame.image.load("Snake/SnakeBody.png"), Direction.Left.value)
    snakeImageTail = pygame.transform.rotate(pygame.image.load("Snake/SnakeTail.png"), Direction.Left.value)
    snake = Snake("Snake", 200, 100, [snakeImageHead], [snakeImageBody], [snakeImageTail], 2, 2)
    camera = Camera(100,0, screen.get_width(), screen.get_height())
    size_map= 3.8
    width = camera.width*size_map
    height = camera.height*size_map
    terrain = sorted([Terrain(Biom.Mouse_cave,100), Terrain(Biom.Spider_cave,200)], key=howDeep)
    print(terrain, "Terrain")
    map = Map(width, height, screen, camera, terrain)
    game = Game(mousePlayerList, snake, map)
    running_loop(game)
init()


