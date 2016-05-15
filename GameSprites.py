""" Inside this class, the most important game sprites are included:
- Reagan(), which is controlled by the player
- FallingMoney(),

"""
import pygame
import pyganim

class Reagan(pygame.sprite.Sprite):
    def __init__(self, screen, screen_size):
        pygame.sprite.Sprite.__init__(self)
        # Image information
        self.standing_pic = pygame.image.load('Images/ronaldus_standing.png').convert()

        # Animated Sprite Information
        self.running = pyganim.PygAnimation([('Images/ronaldus_run_0.png', 0.1),
                                            ('Images/ronaldus_run_1.png', 0.1),
                                            ('Images/ronaldus_run_2.png', 0.1),
                                            ('Images/ronaldus_run_3.png', 0.1),
                                            ('Images/ronaldus_run_4.png', 0.1),
                                            ('Images/ronaldus_run_5.png', 0.1)
                                            ])
        self.running.play()

        self.screen = screen
        self.screen_size = screen_size

        self.pos = [20, 0]
        self.speed = 0


    def update(self):
        self.pos[0] += self.speed
        self.blit_me()

    def move(self, action):
        if action == 'R':
            self.speed = 1
        elif action == 'L':
            self.speed = -1
        elif action == 'RU' or 'LU':
            self.speed = 0

    def blit_me(self):
        if self.speed != 0:
            self.running.blit(self.screen, self.pos)
        else:
            self.screen.blit(self.standing_pic, self.pos)


# For now, we will just use coins
# TODO: Include different values for the game
class FallingMoney(pygame.sprite.Sprite):
    def __init__(self, screen, screen_size, pos, speed, value_point):
        pygame.sprite.Sprite.__init__(self)
        self.spinning_coin = pyganim.PygAnimation([('Images/coin_01.png', .1),
                                                   ('Images/coin_02.png', .1),
                                                   ('Images/coin_03.png', .1),
                                                   ('Images/coin_04.png', .1),
                                                   ('Images/coin_05.png', .1),
                                                   ('Images/coin_06.png', .1),
                                                   ('Images/coin_07.png', .1),
                                                   ('Images/coin_08.png', .1)
                                                   ])
        self.spinning_coin.play()
        # Get the image ready

        # Properties of the falling money here...
        self.pos = pos
        self.speed = speed

        # Info so that we can blit the coin image onto the screen
        self.screen = screen
        self.screen_size = screen_size

    def update(self):
        self.pos[1] += self.speed
        self.blit_me()

    def blit_me(self):
        self.spinning_coin.blit(self.screen, self.pos)


# TODO: Decide if this is necessary
# In more advanced levels, this will have some openings the player has to jump over to get coins
class Floor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)