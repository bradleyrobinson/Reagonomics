# Reagonomics, by Bradley Robinson and Kason Hudman
#

import pygame
import random
import GameSprites
import Levels
import copy


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


def play_level(screen, level, active_sprite_list, reagan):
    play = True
    level_won = True
    while play:
        clock.tick(60)
        play = get_events(reagan)
        level.update()
        level.draw(screen)
        active_sprite_list.update()
        reagan.blit_me()
        pygame.display.flip()
        if reagan.health == 0:
            play = False
            level_won = False
    return level_won


clock = pygame.time.Clock()


def main():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    pygame.init()
    SIZE = [1200, 701]
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
    continue_level = play_level(screen, current_level, active_sprite_list, reagan)
    play = True
    while play:
        while continue_level:
            current_level_no += 1
            current_level = level_list[current_level_no]
            reagan.level = current_level
            continue_level = play_level(screen, current_level, active_sprite_list, reagan)
        else:
            current_level = level_list[current_level_no]
            reagan.health = 3
            reagan.rect.x, reagan.rect.y = current_level.player_pos
            reagan.level = current_level
            continue_level = play_level(screen, current_level, active_sprite_list, reagan)

    pygame.quit()


if __name__ == '__main__':
    main()
