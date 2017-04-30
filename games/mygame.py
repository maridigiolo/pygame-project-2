import pygame
import sys
import random
import time

class Character:
    def __init__(self, name, x, y):
        self.name = name
        self.pos = [x,y]
        self.speed_x = 0
        self.speed_y = 0
        self.pos_ant = None


class Hero(Character):
    def mov(self, x, y):
        new_pos = [0,1]
        new_pos[0] = self.pos[0] + x
        new_pos[1] = self.pos[1] + y
        if new_pos[0] >= 451:
            self.pos[0] = 451
        elif new_pos[0] <= 30:
            self.pos[0] = 30
        else:
            self.pos[0] += x

        if new_pos[1] >= 415:
            self.pos[1] = 415
        elif new_pos[1] <= 30:
            self.pos[1] = 30
        else:
            self.pos[1] += y


class Monster(Character):
    def mov(self):
        #Setting random position
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        #Changing the direction, and setting the speed
        #for x direction
        if x == 0:
            x += 45
        elif x == 1:
            x -= -45
        else:
            x = 0
        #for y direction
        if y == 0:
            y += 45
        elif y == 1:
            y -= -45
        else:
            y = 0

        #Avoiding the last position
        if self.pos + [x,y] == self.pos_ant:
            return
        self.pos_ant = self.pos

        #defining the limits to the moviment inside the screen
        self.pos[0] += x
        if self.pos[0] > 492:
            self.pos[0] = 20
        elif self.pos[0] < 20:
            self.pos[0] = 492


        self.pos[1] += y
        if self.pos[1] > 460:
            self.pos[1] = 20
        elif self.pos[1] < 20:
            self.pos[1] = 460

        #Just to show the new position
        # print(self.pos)

class Goblin(Character):
    def mov(self):
        #Setting random position
        x = random.randint(20, 480)
        y = random.randint(20, 400)
        self.pos[0] += self.speed_x
        self.pos[1] += self.speed_y
        self.speed_x = random.randint(0, 1)
        self.speed_y = random.randint(0, 1)

        #defining the limits to the moviment inside the screen
        self.pos[0] += x
        if self.pos[0] > 492:
            self.pos[0] = 20
        elif self.pos[0] < 20:
            self.pos[0] = 492


        self.pos[1] += y
        if self.pos[1] > 460:
            self.pos[1] = 20
        elif self.pos[1] < 20:
            self.pos[1] = 460


class Game:
    def __init__ (self, screen):
        self.screen = screen
        self.background = pygame.image.load("../images/background.png")
        self.hero_img = pygame.image.load("../images/hero.png")
        self.monster_img = pygame.image.load("../images/monster.png").convert_alpha()
        self.goblin_img = pygame.image.load("../images/goblin.png").convert_alpha()
        #display a message asking if the user wants to play again
        font = pygame.font.SysFont('Papyrus', 20, bold = True)
        self.text = font.render('Hit ENTER to play again!', True, (255, 255, 255))
        fontw = pygame.font.SysFont('Comic Sans MS', 60, bold = True)
        self.textw = fontw.render('WIN!', True, (255, 255, 0))
        fontl = pygame.font.SysFont('Comic Sans MS', 60, bold = True)
        self.textl = fontl.render('GAME OVER!', True, (255, 0, 0))

    def redraw (self, hero, monster, goblins):
        self.screen.blit(self.background, [0,0])
        for g in goblins:
            self.screen.blit(self.goblin_img, [g.pos[0], g.pos[1]])
        if hero:
            self.screen.blit(self.hero_img, [hero.pos[0], hero.pos[1]])
        else:
            self.screen.blit(self.textl, (70,180))
            self.screen.blit(self.text, (250, 390))
        if monster:
            self.screen.blit(self.monster_img, [monster.pos[0], monster.pos[1]])
        else:
            self.screen.blit(self.textw, (170,180))
            self.screen.blit(self.text, (250, 390))

        # Game display
        pygame.display.update()

def wait_for_return ():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'restart'

def is_collided_goblin(rectH, rectGList):
    for rectGoblin in rectGList:
        if rectGoblin.colliderect(rectH):
            return True
    return False

def main():
    width = 512
    height = 480

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('My Game')
    winsound = pygame.mixer.Sound('../sounds/win.wav')
    losesound = pygame.mixer.Sound('../sounds/lose.wav')
    game = Game(screen)
    clock = pygame.time.Clock()

    # Game initialization
    hero = Hero('Hero', 236, 220)
    monster = Monster('Monster', 150, 300 )
    goblins = []
    for i in range(0, 4):
        a = random.randint(20, 480)
        b = random.randint(20, 400)
        new_goblin = Goblin('Goblin', a, b)
        goblins.append(new_goblin)

    #Using time.time() to wait the next moviment
    time_started = time.time()
    next_action_time = time_started

    stop_game = False
    moving = False
    while not stop_game:
        # look through user events fired
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
            # if they closed the window, set stop_game to True
            # to exit the main loop
                stop_game = True

            if event.type == pygame.KEYDOWN:
                moving = True

            elif event.type == pygame.KEYUP:
                moving = False

        # print(moving)
        if moving:
            if event.key == pygame.K_UP:
                hero.mov(0, -3)
            elif event.key == pygame.K_DOWN:
                hero.mov(0, 3)
            elif event.key == pygame.K_RIGHT:
                hero.mov(3, 0)
            elif event.key == pygame.K_LEFT:
                hero.mov(-3, 0)

        # Game logic
        if next_action_time <= (time.time()):
            monster.mov()
            for g in goblins:
                g.mov()
            time_started = time.time()
            next_action_time = time_started + 0.3


        #Decteting the collision (hero_rect position = hero_x, hero_y, hero_width, hero_hight)
        goblins_rect = []
        hero_rect = pygame.Rect((hero.pos[0], hero.pos[1], 32, 32))
        monster_rect = pygame.Rect((monster.pos[0], monster.pos[1], 32, 32))
        for g in goblins:
            goblins_rect.append(pygame.Rect((g.pos[0], g.pos[1], 32, 32)))

        if hero_rect.colliderect(monster_rect):
            winsound.play()
            #make the monster disapear
            game.redraw(hero, None, goblins)
            restart = wait_for_return()
            if restart == 'restart':
                return restart
            else:
                stop_game = True

        elif is_collided_goblin(hero_rect, goblins_rect):
            losesound.play()
            #make the hero disapear
            game.redraw(None, monster, goblins)
            restart = wait_for_return()
            if restart == 'restart':
                return restart
            else:
                stop_game = True

        # Draw background
        game.redraw(hero, monster, goblins)
        clock.tick(60)

    pygame.quit()
    return None

if __name__ == '__main__':
    restart = 'restart'
    while restart == 'restart':
        restart = main()
