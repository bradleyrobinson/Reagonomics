""" Inside this class, the most important game sprites are included:
- Reagan(), which is controlled by the player
- FallingMoney(),

"""
import pygame
import pyganim
import os

GREEN = (10, 255, 10)

class Reagan(pygame.sprite.Sprite):
    def __init__(self, screen, screen_size):
        pygame.sprite.Sprite.__init__(self)
        # Image information
        self.standing_pic = pygame.image.load(os.path.join('Images', 'ronaldus_standing.png')).convert_alpha()
        self.standing_pic.set_colorkey((0, 0, 0))
        # Animated Sprite Information
        self.running_right = pyganim.PygAnimation([(os.path.join('Images', 'ronaldus_run_0.png'), 0.1),
                                             (os.path.join('Images', 'ronaldus_run_1.png'), 0.1),
                                             (os.path.join('Images', 'ronaldus_run_2.png'), 0.1),
                                             (os.path.join('Images', 'ronaldus_run_3.png'), 0.1),
                                             (os.path.join('Images', 'ronaldus_run_4.png'), 0.1),
                                             (os.path.join('Images', 'ronaldus_run_5.png'), 0.1)])
        
        self.running_left = pyganim.PygAnimation([(os.path.join('Images', 'ronaldus_runleft_0.png'), 0.1),
                                                  (os.path.join('Images', 'ronaldus_runleft_1.png'), 0.1),
                                                  (os.path.join('Images', 'ronaldus_runleft_2.png'), 0.1),
                                                  (os.path.join('Images', 'ronaldus_runleft_3.png'), 0.1),
                                                  (os.path.join('Images', 'ronaldus_runleft_4.png'), 0.1),
                                                  (os.path.join('Images', 'ronaldus_runleft_5.png'), 0.1)])

        # These assure that the images are animated
        self.running_right.play()
        self.running_left.play()

        self.is_running = False
        self.image = self.standing_pic

        # These give us information for where to put things
        self.rect = self.standing_pic.get_rect()
        self.screen = screen
        self.screen_size = screen_size

        # These give us position info
        # self.pos = [20, 0]
        self.speed_x = 0
        self.speed_y = 0


        # A list of sprites we can bump against
        self.level = None

    def update(self):
        # self.pos[0] += self.speed_x
        # TODO: Change this to see if it works better...
        self.calc_grav()
        self.rect.x += self.speed_x
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.speed_x > 0:
                self.rect.right = block.rect.left
            elif self.speed_x < 0:
                self.rect.left = block.rect.right
        self.rect.y += self.speed_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            if self.speed_y > 0:
                self.rect.bottom = block.rect.top
            elif self.speed_y < 0:
                self.rect.top = block.rect.bottom
            self.speed_y = 0
        self.check_for_platforms()
        # self.pos[1] += self.speed_y

#        self.blit_me()

    def check_for_platforms(self):
        pass

    def move(self, action):
        if action == 'R':
            self.speed_x = 7
        elif action == 'L':
            self.speed_x = -7
        elif action == 'J':
            self.jump()
        elif action == 'S':
            self.speed_x *= 1.5
        elif action == 'RU' or 'LU':
            self.speed_x = 0
        elif action == 'SU':
            self.is_running = False

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.screen_size[1]:
            self.speed_y = - 20

    def calc_grav(self):
        if self.speed_y == 0:
            self.speed_y = 2.5
        else:
            self.speed_y += 1.5

        # Unless we are on the ground.
        # TODO: Change this to just platforms
        if self.rect.y >= self.screen_size[1] - self.rect.height and self.speed_y >= 0:
            self.speed_y = 0
            self.rect.y = self.screen_size[1] - self.rect.height

    def blit_me(self):
        if self.speed_x > 0:
            self.running_right.blit(self.screen, self.rect)
        elif self.speed_x < 0:
            self.running_left.blit(self.screen, self.rect)
        else:
            self.screen.blit(self.standing_pic, self.rect)


# For now, we will just use coins
# TODO: Include different values for the game
class FallingMoney(pygame.sprite.Sprite):
    def __init__(self, screen, screen_size, pos, speed, value_point):
        pygame.sprite.Sprite.__init__(self)
        self.spinning_coin = pyganim.PygAnimation([
                                                   (os.path.join('Images', 'coin_02.png'), 0.1),
                                                   (os.path.join('Images', 'coin_03.png'), 0.1),
                                                   (os.path.join('Images', 'coin_04.png'), 0.1),
                                                   (os.path.join('Images', 'coin_05.png'), 0.1),
                                                   (os.path.join('Images', 'coin_06.png'), 0.1),
                                                   (os.path.join('Images', 'coin_07.png'), 0.1),
                                                   (os.path.join('Images', 'coin_08.png'), 0.1)
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


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()