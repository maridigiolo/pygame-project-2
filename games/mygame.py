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
            x += 40
        elif x == 1:
            x -= -40
        else:
            x = 0
        #for y direction
        if y == 0:
            y += 40
        elif y == 1:
            y -= -40
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
            time_started = time.time()
            next_action_time = time_started + 0.4


        #Decteting the collision
        #hero_rect position = hero_x, hero_y, hero_width, hero_hight
        hero_rect = pygame.Rect((hero.pos[0], hero.pos[1], 32, 32))
        monster_rect = pygame.Rect((monster.pos[0], monster.pos[1], 32, 32))
        # print(hero_rect)
        # print(monster_rect)
        if hero_rect.colliderect(monster_rect):


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pass
                else:
                    stop_game = True



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
