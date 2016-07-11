import pygame
import GameSprites
import os
import random


class Level(object):
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.money_list = pygame.sprite.Group()
        self.player = player
        # Here are variables that must be defined in the Level child, assuring that the level makes sense and works
        self.player_pos = None
        self.background = None
        self.coin_frequency = None
        self.coin_amount = None
        self.coin_total = None
        self.current_coin_count = 0
        self.player_score = 0
        self.level_speed_range = 0
        self.countdown = None
        # This lets us calculate the current_time

    # TODO: Keep track of the time the player has been in the level,
    # and cap that level to a certain time, so they don't die everytime

    def update(self):
        self.countdown -= .05
        self.coin_generation()
        self.platform_list.update()
        self.player_score = self.player.score
        self.enemy_list.update()
        self.money_list.update()

    def coin_generation(self):
        # TODO: Make the coin generation dependent on time, and only use the coin_frequency variable as a cap for the
        # screen
        if len(self.money_list) < self.coin_frequency and self.current_coin_count < self.coin_total:
            money_pos = [random.randrange(0, 1100, 20), random.randrange(-10, 0)]
            speed = random.uniform(self.level_speed_range[0], self.level_speed_range[1])
            self.level_speed_range[1] += .02
            money = GameSprites.FallingMoney(money_pos, speed, 0)
            self.money_list.add(money)
            self.current_coin_count += 1

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((255, 255, 255))
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.money_list.draw(screen)
        self.player.update()

    # The following functions must be present in all levels
    # TODO: It seems that there is a little bug here, after falling a certain amount of times coins no longer re-appear
    def reset(self):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.money_list = pygame.sprite.Group()
        self.set_level()
        self.player.score = 0

    def set_level(self):
        pass


class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """
        Level.__init__(self, player)
        self.set_level()

    def set_level(self):
        # coin_frequency, coin_amount, coin_total
        # Array with width, height, x, and y of platform
        level = [[370, 70, 0, 630],
                 [210, 70, 520, 630],
                 [370, 70, 840, 630],
                 ]

        self.background = pygame.image.load(os.path.join("Images", "reaganomics_background.png"))
        self.player_pos = [10, 500]
        self.coin_frequency = 10
        self.coin_amount = 6
        self.coin_total = 100
        # self.start_time = start_time
        self.level_speed_range = [2, 5]
        self.countdown = 60

        for platform in level:
            block = GameSprites.Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


# TODO: Correct this level to make sure that it follows the correct pattern. It is a test, so it all can be scrapped.
# In fact, this level currently just crashes.
class Level2(Level):
    def __init__(self, player):
        Level.__init__(self, player)

        #Here are the platforms
        level = [[350, 70, 0, 630],
                 [210, 70, 520, 490],
                 [370, 70, 840, 630],
                 ]

        self.background = pygame.image.load(os.path.join("Images", "reaganomics_background.png"))
        self.player_pos = [10, 500]

        # Just a test

        for i in range(20):
            money_pos = [random.randrange(0, 1100, ), random.randrange(-1000, -10, 500)]
            speed = i / 2
            money = GameSprites.FallingMoney(money_pos, speed, 0)
        # Just a test:
        for i in range(1, 51):
            print i
            money_pos = [random.randrange(0, 1000), random.randrange(-10000, -20, 20)]
            speed = i / 2.0
            money = GameSprites.FallingMoney(money_pos, speed, 1)
            self.money_list.add(money)
        # Go through the array above and add platforms
        for platform in level:
            block = GameSprites.Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)