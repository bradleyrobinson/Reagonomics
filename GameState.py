"""
This class will help us keep track of where we are!
GameStatus will keep track of how fast the money should fall, points, where the player stands, etc.
The GameStatus will hold a player object, so we can keep track of who is playing, and where they're at.
"""


class GameStatus:
    def __init__(self):
        pass


class Player:
    def __init__(self, player_name):
        self.score = 0
        self.player_name = player_name

    def increase_score(self, score):
        self.score += score


