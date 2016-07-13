""" Inside this class, the most important game sprites are included:
- Reagan(), which is controlled by the player
- FallingMoney(),

"""
import pygame
import pyganim
import os
import random

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

        self.jumping = pyganim.PygAnimation([(os.path.join('Images', 'ronaldus_jump_0.png'), 10),
                                             (os.path.join('Images', 'ronaldus_jump_1.png'), 0.01),
                                             (os.path.join('Images', 'ronaldus_jump_2.png'), 0.01)])

        self.jumping_left = pyganim.PygAnimation([(os.path.join('Images', 'ronaldus_jump_0_left.png'), 10),
                                                  (os.path.join('Images', 'ronaldus_jump_1.png'), 0.01),
                                                  (os.path.join('Images', 'ronaldus_jump_2.png'), 0.01)])






        # These assure that the images are animated
        self.running_right.play()
        self.running_left.play()
        self.jumping.play()
        self.jumping_left.play()

        self.is_running = 1

        # These give us information for where to put things
        self.rect = self.standing_pic.get_rect()
        self.screen = screen
        self.screen_size = screen_size

        # These give us position info
        self.speed_x = 0
        self.speed_y = 0
        self.health = 3
        self.right_down = False
        self.left_down = False

        # Total points:
        self.total_money = 0
        self.score = 0

        # A list of sprites we can bump against
        self.level = None

    def update(self):
        self.update_health()
        self.calc_grav()
        self.rect.x += self.speed_x * self.is_running
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
        self.get_money()

    def get_money(self):
        money_hit_list = pygame.sprite.spritecollide(self, self.level.money_list, True)
        for money in money_hit_list:
            self.score += 5
            #Coin collecting sound
            money_sound = pygame.mixer.Sound(os.path.join('Sounds', 'coin5.ogg'))
            money_sound.set_volume(.1)
            money_sound.play()


    def move(self, action):
        if action == 'R':
            self.right_down = True
            self.speed_x = 8
        elif action == 'L':
            self.left_down = True
            self.speed_x = -8
        elif action == 'J':
            self.jump()
        # TODO: Let's change this sometime soon... It doesn't work yet, or maybe let's do without this.
        #elif action == 'S':
        #    self.is_running = 1.5
        elif action == 'RU':
            self.right_down = False
            if self.left_down is True:
                self.speed_x = -8
            else:
                self.speed_x = 0
        elif action == 'LU':
            self.left_down = False
            if self.right_down is True:
                self.speed_x = 8
            else:
                self.speed_x = 0
        elif action == 'SU':
            self.is_running = 1
        self.last_action = action

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= self.screen_size[1]:
            self.speed_y = - 24

    def calc_grav(self):
        if self.speed_y == 0:
            self.speed_y = 2.5
        else:
            self.speed_y += 1.5

        # Unless we are on the ground.
        # TODO: Change this to just platforms
        #if self.rect.y >= self.screen_size[1] - self.rect.height and self.speed_y >= 0:
        #    self.speed_y = 0
        #    self.rect.y = self.screen_size[1] - self.rect.height

    def blit_me(self):
        if self.speed_x > 0 and self.speed_y == 0:
            self.running_right.blit(self.screen, self.rect)
        elif self.speed_x < 0 and self.speed_y == 0:
            self.running_left.blit(self.screen, self.rect)
        elif self.speed_y< 0 and self.speed_x < 0:
            self.jumping_left.blit(self.screen, self.rect)
        elif self.speed_y < 0:
            self.jumping.blit(self.screen, self.rect)
        else:
            self.screen.blit(self.standing_pic, self.rect)

    def update_health(self):
        if self.rect.y >= self.screen_size[1] - self.rect.height and self.speed_y >= 0:
            self.health = 0


# For now, we will just use coins
# TODO: Include different values for the game
class FallingMoney(pygame.sprite.Sprite):
    def __init__(self, pos, speed, current_level):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Images', 'coin_01.png'))
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
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        # We get the level so that we can let the object know when things have fallen off the screen
        self.current_level = current_level

    def update(self):
        self.rect.y += self.speed
        # If the coin goes below the screen, reposition it randomly and add to the levels coins dropped.
        if self.rect.y > 701:
            self.current_level.coins_dropped += 1
            money_reset_y = random.randrange(-100, -10)
            money_reset_x = random.randrange(0, 1100)
            self.rect.y = money_reset_y
            self.rect.x = money_reset_x

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()