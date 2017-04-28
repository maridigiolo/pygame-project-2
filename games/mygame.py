import pygame
import sys
import random
import time


class Hero:
    def __init__(self, name, x, y):
        self.name = name
        self.pos = [x, y]

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


class Monster:
    def __init__(self, name, x, y):
        self.name = name
        self.pos = [x, y]
        self.pos_ant = None

    def mov(self):
        #Setting random position
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        #Changing the direction, and setting the speed
        #for x direction
        if x == 0:
            x = 30
        elif x == 1:
            x = -30
        else:
            x = 0
        #for y direction
        if y == 0:
            y = 30
        elif y == 1:
            y = -30
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
        print(self.pos)


def main():
    width = 512
    height = 480
    blue_color = (97, 159, 182)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('My Game')
    clock = pygame.time.Clock()
    background = pygame.image.load("../images/background.png")
    hero_img = pygame.image.load("../images/hero.png")
    monster_img = pygame.image.load("../images/monster.png").convert_alpha()


    # Game initialization
    hero = Hero('Hero', 236, 220)
    monster = Monster('Monster', 150, 300 )

    #Using time.time() to wait the next moviment
    time_started = time.time()
    next_action_time = time_started + 2

    #If you hold on the key, you gonna make moviment continuous
    pygame.key.set_repeat(10)

    stop_game = False
    while not stop_game:
        # look through user events fired
        for event in pygame.event.get():
            # Event handling
            if event.type == pygame.QUIT:
            # if they closed the window, set stop_game to True
            # to exit the main loop
                stop_game = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    hero.mov(0, -20)
                elif event.key == pygame.K_DOWN:
                    hero.mov(0, 20)
                elif event.key == pygame.K_RIGHT:
                    hero.mov(20, 0)
                elif event.key == pygame.K_LEFT:
                    hero.mov(-20, 0)


        # Game logic
        if next_action_time <= int(time.time()):
            monster.mov()
            time_started = time.time()
            next_action_time = int(time_started) + 2

        pygame.display.update()

        # Draw background
        screen.fill(blue_color)
        screen.blit(background, [0,0])
        screen.blit(hero_img, [hero.pos[0], hero.pos[1]])
        screen.blit(monster_img, [monster.pos[0], monster.pos[1]])

        # Game display

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
