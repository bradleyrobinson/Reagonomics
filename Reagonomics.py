# Reagonomics, by Bradley Robinson and Kason Hudman
#

import pygame
import random
import GameSprites

BLACK = (0, 0, 0)

pygame.init()
SIZE = [800, 600]
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Reagonomics')
reagan = GameSprites.Reagan(screen, SIZE)


def control_player(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            return 'R'
        elif event.key == pygame.K_LEFT:
            return 'L'
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            return 'RU'
        elif event.key == pygame.K_LEFT:
            return 'LU'


def get_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        else:
            reagan.move(control_player(event))
    return True


def main():
    play = True
    while play:
        play = get_events()
        screen.fill(BLACK)
        reagan.update()
        pygame.display.flip()


if __name__ == '__main__':
    main()
