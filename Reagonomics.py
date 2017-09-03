# Reagonomics, by Bradley Robinson and Kason Hudman
#
# NOTE: This section is deprecated!

import pygame
import GameSprites
import Levels
import GameState


def main():
    game = GameState.Game()
    game.game_loop()
    pygame.quit()

if __name__ == '__main__':
    main()
