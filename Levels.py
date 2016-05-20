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
        self.player_pos = None
        self.background = None

    def update(self):
        self.platform_list.update()
        self.enemy_list.update()
        self.money_list.update()

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((255, 255, 255))
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.money_list.draw(screen)
        self.player.update()


class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        level = [[370, 70, 0, 630],
                 [210, 70, 520, 630],
                 [370, 70, 840, 630],
                 ]

        self.background = pygame.image.load(os.path.join("Images", "reaganomics_background.png"))
        self.player_pos = [10, 500]

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

