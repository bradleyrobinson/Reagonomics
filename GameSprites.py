""" Inside this class, the most important game sprites are included:
- Reagan(), which is controlled by the player
- FallingMoney(),

"""
import os
import random
import pygame
import pyganim

GREEN = (10, 255, 10)


class Reagan(pygame.sprite.Sprite):
    """This is the player that makes it all happen! Includes all the display and movement logic.

    Attributes
    ----------
    standing_pic : pygame.image
        The image of Reagan just standing there
    running_right : pyganim.PygAnimation
        The animation of Reagan running right
    running_left : pyganim.PygAnimation
        Take a wild guess here
    jumping : pyganim.PygAnimation
        Reagan... jumping
    
    """
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
        self.is_revolution = False
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
        # Calculates whether we are touching something
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
        for _ in money_hit_list:
            self.score += 5
            #Coin collecting sound
            money_sound = pygame.mixer.Sound(os.path.join('Sounds', 'coin5.ogg'))
            money_sound.set_volume(.1)
            money_sound.play()


    def move(self, action):
        if action == 'R':
            if (self.rect.x + self.rect.width) >= (self.screen_size[0]):
                self.speed_x = 0
            else:
                self.right_down = True
                self.speed_x = 8
        elif action == 'L':
            self.left_down = True
            if self.rect.x <= 0:
                self.speed_x = 0
            else:
                self.speed_x = -8
        elif action == 'J':
            self.jump()
        if action == 'RU':
            self.right_down = False
            if self.left_down is True:
                self.speed_x = -8
            else:
                self.speed_x = 0
        elif action == 'LU':
            self.left_down = False
            if self.right_down is True and (self.rect.x + self.rect.width) < (self.screen_size[0]):
                self.speed_x = 8
                pass
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

    def update_health(self, is_revolution=False):
        if self.rect.y >= self.screen_size[1] - self.rect.height and self.speed_y >= 0:
            self.health = 0
        if is_revolution:
            self.health = 0
            self.is_revolution = True
        elif not is_revolution:
            self.is_revolution = False


# For now, we will just use coins
# TODO: Include different values for the game, but this is much later when the game is running well
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
        self.left = pygame.image.load(os.path.join('Images', 'plat1.png'))
        self.middle = pygame.image.load(os.path.join('Images', 'plat2.png'))
        self.right = pygame.image.load(os.path.join('Images', 'plat3.png'))
        self.left.set_colorkey((0, 0, 0,))
        self.middle.set_colorkey((0, 0, 0))
        self.right.set_colorkey((0, 0, 0))
        self.image = pygame.Surface([width*128, height*93])
        self.image.set_colorkey((0, 0, 0))
        if width == 2:
            self.image.blit(self.left, [0,0])
            self.image.blit(self.right, [128,0])
        elif width > 2:
            self.image.blit(self.left, [0,0])
            for i in range (1, width-1):
                self.image.blit(self.middle, [128*i, 0])
            self.image.blit(self.right, [(width-1)*128,0])
        self.rect = self.image.get_rect()
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, current_level, life):
        pygame.sprite.Sprite.__init__(self)
        self.current_level = level
        self.life = life

    
    def update(self):
        pass



