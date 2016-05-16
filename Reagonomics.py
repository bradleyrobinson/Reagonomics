# Reagonomics, by Bradley Robinson and Kason Hudman
#

import pygame
import random
import GameSprites
import Levels


# Function that determines if an important
def control_player(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RIGHT:
            return 'R'
        elif event.key == pygame.K_LEFT:
            return 'L'
        elif event.key == pygame.K_UP:
            return 'J'
        elif event.key == pygame.K_LSHIFT:
            return 'S'
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_RIGHT:
            return 'RU'
        elif event.key == pygame.K_LEFT:
            return 'LU'
        elif event.key == pygame.K_LSHIFT:
            return 'SU'


# This figures out if the game is to be closed, if not, it sends the rest of the events to control the player
def get_events(reagan):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        else:
            reagan.move(control_player(event))
    return True

clock = pygame.time.Clock()
def main():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    pygame.init()
    SIZE = [800, 600]
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Reagonomics')
    reagan = GameSprites.Reagan(screen, SIZE)
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(reagan)
    current_level_no = 0
    level_1 = Levels.Level_01(reagan)
    level_list = [level_1]
    current_level = level_list[current_level_no]
    reagan.level = current_level
    play = True
    while play:
        clock.tick(60)
        play = get_events(reagan)
        screen.fill(WHITE)
        current_level.update()
        current_level.draw(screen)
        active_sprite_list.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
