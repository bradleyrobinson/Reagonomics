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
sprite_list = [reagan]


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


# TODO: This is just for testing
def place_coints():
    for i in range(0, 20):
        position = [random.randrange(0, SIZE[0]), random.randrange(0, SIZE[1])]
        speed = .2
        coin = GameSprites.FallingMoney(screen, SIZE, position, speed, 10)
        sprite_list.append(coin)

def main():
    play = True
    place_coints()
    while play:
        play = get_events()
        screen.fill(BLACK)
        for sprite in sprite_list:
            sprite.update()
        pygame.display.flip()


if __name__ == '__main__':
    main()
