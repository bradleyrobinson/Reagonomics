# Reagonomics, by Bradley Robinson and Kason Hudman
#
# NOTE: This section is deprecated!

import pygame
import GameSprites
import Levels
import GameState


"""
pygame.init()
font = pygame.font.SysFont('Calibri', 34)


# Function that determines what keys have been pressed
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
        time_passed = clock.tick_busy_loop(60)
        play = get_events(reagan)
        level.update()
        # TODO: Cleanup here, make one constant for the text color
        countdown_text = font.render("Time Remaining: " + str(int(level.countdown)), 1, (0, 0, 0))
        current_score_text = font.render("Level Score: " + str(int(level.player_score)), 1, (0, 0, 0))
        level.draw(screen)
        active_sprite_list.update()
        reagan.blit_me()
        screen.blit(countdown_text, [100, 100])
        screen.blit(current_score_text , [100, 130])
        pygame.display.flip()
        if reagan.health == 0:
            play = False
            level_won = False
            level.death_screen(screen, font, clock)
        elif level.countdown <= 0:
            play = False
            level_won = True
    return level_won


clock = pygame.time.Clock() J


def main():
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    SIZE = [1200, 701]
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Reagonomics')
    reagan = GameSprites.Reagan(screen, SIZE)
    active_sprite_list = pygame.sprite.Group()
    active_sprite_list.add(reagan)
    current_level_no = 0
    level_1 = Levels.Level_01(reagan, screen, SIZE)
    level_2 = Levels.Level2(reagan, screen, SIZE)
    level_list = [level_1, level_2]
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
            current_level.reset()
            reagan.rect.x, reagan.rect.y = current_level.player_pos
            reagan.level = current_level
            continue_level = play_level(screen, current_level, active_sprite_list, reagan)

    pygame.quit()


"""

def main():
    game = GameState.Game()
    game.game_loop()
    pygame.quit()

if __name__ == '__main__':
    main()
