"""
This class will help us keep track of where we are!
GameStatus will keep track of how fast the money should fall, points, where the player stands, etc.
The GameStatus will hold a player object, so we can keep track of who is playing, and where they're at.
"""
import pygame
import GameSprites
import random

class GameStatus:
    def __init__(self, screen, screen_size):
        self.current_player = Player('NA')
        self.playing = False
        self.money_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        # TODO: Let's figure out how we're going to arrange the levels
        # But wait, this is important but not too important now
        self.status = 0
        self.current_level = 0

        #Here is the screen information
        self.screen = screen
        self.screen_size = screen_size

    # TODO: This will eventually get all the information needed
    # for the level, so that during gameplay we can display the proper level
    def insert_money(self, level):
        for i in range(0, level):
            position = [random.randrange(0, self.screen_size[0]), 0]
            speed = .2
            coin = GameSprites.FallingMoney(self.screen, self.screen_size, position, speed, 10)
            self.money_list.add(coin)


class Player:
    def __init__(self, player_name):
        self.score = 0
        self.player_name = player_name

    def increase_score(self, score):
        self.score += score


