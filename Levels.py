import pygame
import GameSprites
import os
import random

pygame.mixer.pre_init(44100, 16, 2, 4096)


class ClassConscience:
    def __init__(self):
        self.needle_position = 0
        self.move_needle_to = 0
        self.bar_image = pygame.image.load(os.path.join('Images', 'class_conscience.png')).convert_alpha()
        self.needle_image = pygame.image.load(os.path.join('Images', 'needle.png')).convert_alpha()
        self.bar_image.set_colorkey((0, 0, 0))
        self.needle_image.set_colorkey((0, 0, 0))
        self.revolution_point = 0

    def reset(self):
        self.needle_position = 0
        self.move_needle_to = 0

    def is_revolution(self):
        if self.needle_position > (self.bar_image.get_rect()[2] - self.needle_image.get_rect()[2]):
            return True
        else:
            return False

    def draw(self, screen):
        screen.blit(self.bar_image, (400, 200))
        # TODO: Fix the positioning on this
        if self.needle_position < self.move_needle_to:
            self.needle_position += .5
        screen.blit(self.needle_image, (400+self.needle_position, 200))


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
    def __init__(self, player, screen, screen_size):
        self.screen = screen

        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.money_list = pygame.sprite.Group()
        self.player = player
        # This is for the dimmer effect.
        self.dimmer = Dimmer()
        self.screen_size = screen_size

        # This variable is modified whenever a coin is not caught:
        self.coins_dropped = 0
        # This is a health like bar indicating how many coins made it to the working class:
        # TODO: Everything with class conscience.
        # This is just a proof of concept.
        self.working_class = ClassConscience()

        # variables that must be defined in any child of Level child
        self.player_pos = None
        self.background = None
        # Coin related stuff
        self.coin_frequency = None
        self.coin_amount = None
        self.coin_total = None
        self.current_coin_count = 0

        # Level holds the local state (level state) of the game
        self.player_score = 0
        self.level_speed_range = []
        self.countdown = None

        self.song = "Sounds/BonzoGoestoBitburg.ogg"
        # Each time the level is reset we want to reset the objects to their
        # original state, and raw coordinates and data are a simple way to
        # guarantee that they will be the same each time
        self.platform_raw_coordinates = []
        self.enemy_raw_data = []

    def update(self):
        self.countdown -= .05
        self.coin_generation()
        self.platform_list.update()
        self.player_score = self.player.score
        self.enemy_list.update()
        self.money_list.update()
        self.working_class.move_needle_to = self.coins_dropped*4
        if self.working_class.is_revolution():
            self.player.update_health(is_revolution=True)

    def coin_generation(self):
        # TODO: Make the coin generation dependent on time, and only use the coin_frequency variable as a cap for the
        # screen
        if len(self.money_list) < self.coin_frequency and self.current_coin_count < self.coin_total:
            money_pos = [random.randrange(0, 1100, 20), random.randrange(-10, 0)]
            speed = random.uniform(self.level_speed_range[0], self.level_speed_range[1])
            self.level_speed_range[1] += .02
            money = GameSprites.FallingMoney(money_pos, speed, self)
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
        self.working_class.draw(self.screen)

    def reset(self):
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.money_list = pygame.sprite.Group()
        self.current_coin_count = 0
        self.player_score = 0
        self.coins_dropped = 0
        self.set_level()
        self.player.score = 0
        self.working_class.reset()

    # TODO: Get this working so the player can continue or leave the game
    @staticmethod
    def death_decision():
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
        # TODO: Figure out why the proletariat screen doesn't show up.
        if not self.player.is_revolution:
            death_string = "Mistakes were made."
        else:
            death_string = "The proletariat has arisen!"
        death_text = font.render(death_string, 1, (255, 255, 255))
        end_darkness = 100
        for i in range(0, end_darkness):
            # Uses the dimmer class
            self.dimmer.dim(darken_factor=i)
            clock.tick_busy_loop(60)
            screen.blit(death_text, [(self.screen_size[0]/2-font.size(death_string)[0]/2), self.screen_size[1]/2])
            pygame.display.flip()

        # continue_game = False
        # while not continue_game:
        #     self.dimmer.dim(darken_factor=end_darkness)
        #     continue_game, decision = self.death_decision()

    def set_level(self):
        pygame.mixer.music.load(self.song)
        pygame.mixer.music.set_volume(0.9)
        pygame.mixer.music.play(-1)
        self.set_platforms()
        self.set_enemies()

    def set_platforms(self):
        for platform in self.platform_raw_coordinates:
            block = GameSprites.Platform(*platform)
            block.player = self.player
            self.platform_list.add(block)

    def set_enemies(self):
        for enemy in self.enemy_raw_data:
            enemy_sprite = enemy.enemy_object(enemy.x, enemy.y, enemy.end_x, enemy.direction)
            self.enemy_list.add(enemy_sprite)


class Level1(Level):
    """ Definition for level 1. """

    def __init__(self, player, screen, screen_size):
        """ Create level 1. """
        Level.__init__(self, player, screen, screen_size)
        self.platform_raw_coordinates = [[3, 1, 0, 630],
                                         [2, 1, 520, 630],
                                         [3, 1, 840, 630],
                                         ]
        self.enemy_raw_data = [
            # they are magic number for now, Sandanista height=79, width=92, block width=128
            GameSprites.EnemyData(GameSprites.Sandanista, 520, 630-79, (520, 520+(128*2)-92), 1)
        ]
        self.level_speed_range = [2, 5]
        self.background = pygame.image.load(os.path.join("Images", "reaganomics_background.png"))
        self.player_pos = [10, 500]
        self.coin_frequency = 10
        self.coin_amount = 6
        self.coin_total = 100

        # TODO: Change the time, this is for testing purposes
        self.countdown = 45

        self.set_level()


class Level2(Level):
    def __init__(self, player, screen, screen_size):
        """ Create level 1. """
        Level.__init__(self, player, screen, screen_size)
        self.platform_raw_coordinates = [[3, 1, 0, 630],
                                         [2, 1, 520, 490],
                                         [3, 1, 840, 630],
                                         ]
        self.background = pygame.image.load(os.path.join("Images", "reaganomics_background.png"))
        self.player_pos = [10, 500]
        self.coin_frequency = 9
        self.coin_amount = 6
        self.coin_total = 100
        # self.start_time = start_time
        self.level_speed_range = [5, 10]
        self.countdown = 60

        Level.set_level(self)


class Level3(Level):
    def __init__(self, player, screen, screen_size):
        """ Create level 1. """
        Level.__init__(self, player, screen, screen_size)
        self.platform_raw_coordinates = [[3, 1, 0, 630],
                                         [1, 1, 520, 630],
                                         [3, 1, 840, 630],
                                         [1, 1, 340, 400],
                                         [1, 1, 550, 300]
                                         ]

        self.background = pygame.image.load(os.path.join("Images", "reaganomics_background.png"))
        self.player_pos = [10, 500]
        self.coin_frequency = 10
        self.coin_amount = 6
        self.coin_total = 100

        self.level_speed_range = [10, 20]
        self.countdown = 45

        self.set_platforms()
