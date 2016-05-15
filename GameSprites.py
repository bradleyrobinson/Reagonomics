""" Inside this class, the most important game sprites are included:
- Reagan(), which is controlled by the player
- FallingMoney(),

"""
import pygame

class Reagan(pygame.sprite.Sprite):
    def __init__(self, screen, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('reagan.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.screen = screen
        self.screen_size = screen_size

        self.pos = [50, (screen_size[1] - 100)]
        self.speed = 0

    def update(self):
        self.pos[0] += self.speed
        self.blit_me()

    def move(self, action):
        if action == 'R':
            self.speed = .1
        elif action == 'L':
            self.speed = -.1
        elif action == 'RU' or 'LU':
            self.speed = 0

    def blit_me(self):
        self.screen.blit(self.image, self.pos)


# For now, we will just use coins
# TODO: Include different values for the game
class FallingMoney(pygame.sprite.Sprite):
    def __init__(self, screen, screen_size, pos, speed, value_point):
        pygame.sprite.Sprite.__init__(self)

        # Get the image ready
        self.image = pygame.image.load('coin_01.jpg')
        pygame.image.set_colorkey((255, 255, 255))

        # Properties of the falling money here...
        self.pos = pos
        self.speed = speed

        # Info so that we can blit the coin image onto the screen
        self.screen = screen
        self.screen_size = screen_size


# TODO: Decide if this is necessary
# In more advanced levels, this will have some openings the player has to jump over to get coins
class Floor(pygame.sprite.Sprite):
    def __init__(self):
        pass