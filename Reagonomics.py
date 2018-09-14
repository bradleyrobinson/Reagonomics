"""
Reagonomics, by Bradley Robinson and Kason Hudman
"""

import pygame
import GameState


def main():
    game = GameState.Game()
    game.game_loop()
    pygame.quit()

if __name__ == '__main__':
    main()
