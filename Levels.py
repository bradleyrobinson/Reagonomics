import pygame
import GameSprites
import os
import random


class Dimmer:
    def __init__(self, keepalive=0):
        self.keepalive = keepalive
        if self.keepalive:
            self.buffer = pygame.Surface(pygame.display.get_surface().get_size())
        else:
            self.buffer = None

    def dim(self, darken_factor=64, color_filter=(0, 0, 0)):
        if not self.keepalive:
            self.buffer = pygame.Surface(pygame.display.get_surface().get_size())
        self.buffer.blit(pygame.display.get_surface(), (0, 0))
        if darken_factor > 0:
            darken = pygame.Surface(pygame.display.get_surface().get_size())
            darken.fill(color_filter)
            darken.set_alpha(darken_factor)
            # safe old clipping rectangle...
            old_clip = pygame.display.get_surface().get_clip()
            # ..blit over entire screen...
            pygame.display.get_surface().blit(darken, (0, 0))
            pygame.display.flip()
            # ... and restore clipping
            pygame.display.get_surface().set_clip(old_clip)

    def undim(self):
        if self.buffer:
            pygame.display.get_surface().blit(self.buffer, (0, 0))
            pygame.display.flip()
            if not self.keepalive:
                self.buffer = None



class Level(object):
    def __init__(self, player, screen_size):
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
        # This is for the dimmer effect.
        self.dimmer = Dimmer()
        self.screen_size = screen_size
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
    def reset(self):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.money_list = pygame.sprite.Group()
        self.current_coin_count = 0
        self.player_score = 0
        self.level_speed_range = 0
        self.set_level()
        self.player.score = 0

    def death_decision(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.type == pygame.K_SPACE:
                    return True, True
                elif event.type == pygame.K_ESCAPE:
                    return True, False
        return False, False

    def death_screen(self, screen, font, clock):
        death_string = "Mistakes were made."
        death_text = font.render(death_string, 1, (255, 255, 255))
        end_darkness = 100
        for i in range(0, end_darkness):
            # Uses the dimmer class
            self.dimmer.dim(darken_factor=i)
            clock.tick_busy_loop(60)
            screen.blit(death_text, [(self.screen_size[0]/2-font.size(death_string)[0]/2), self.screen_size[1]/2])
            pygame.display.flip()
        """ This will be awesome!
        continue_game = False
        while not continue_game:
            self.dimmer.dim(darken_factor=end_darkness)
            continue_game, decision = self.death_decision()
        """
    def set_level(self):
        pass


class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player, screen_size):
        """ Create level 1. """
        Level.__init__(self, player, screen_size)
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
        # TODO: Change the time, this is for testing purposes
        self.countdown = 10

        for platform in level:
            block = GameSprites.Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


# TODO: Correct this level to make sure that it follows the correct pattern. It is a test, so it all can be scrapped.
# In fact, this level currently just crashes.
class Level2(Level):
    def __init__(self, player, screen_size):
        """ Create level 1. """
        Level.__init__(self, player, screen_size)
        self.set_level()

    def set_level(self):
        #Here are the platforms
        level = [[350, 70, 0, 630],
                 [210, 70, 520, 490],
                 [370, 70, 840, 630],
                 ]

        self.background = pygame.image.load(os.path.join("Images", "reaganomics_background.png"))
        self.player_pos = [10, 500]
        self.coin_frequency = 10
        self.coin_amount = 6
        self.coin_total = 100
        # self.start_time = start_time
        self.level_speed_range = [2, 5]
        # TODO: Change the time, this is for testing purposes
        self.countdown = 10

        for platform in level:
            block = GameSprites.Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
