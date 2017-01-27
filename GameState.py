"""
This class will help us keep track of where we are!
GameStatus will keep track of how fast the money should fall, points, where the player stands, etc.
The GameStatus will hold a player object, so we can keep track of who is playing, and where they're at.
"""
import pygame
import GameSprites
import Levels
import random


# TODO: We need to take everything in the Reagonomics file and basically structure it here. There will be a class,
# which will include the stuff that Pygame needs to run. This will centralize all important variables and objects so
# we don't have to do weird backward calls.
class Game:
    def __init__(self):
        pygame.init()
        # TODO: Use the pygame.font.Font instead, since it is better with PyInstall package
        self.font = pygame.font.SysFont('Calibri', 34)

        # Screen information
        self.SIZE = [1200, 701]
        self.screen = pygame.display.set_mode(self.SIZE)
        pygame.display.set_caption('Reagonomics')

        self.clock = pygame.time.Clock()

        # Input information
        self.ginput = GameInput()
        # TODO: When the menu is ready, change this to "MENU"
        self.game_state = "PLAY"

        self.pause_menu = PauseMenu(self.screen, self.font, self.SIZE)
        # Player information
        self.reagan = GameSprites.Reagan(self.screen, self.SIZE)

        # Level information
        # TODO: As levels are created, add them here
        level_1 = Levels.Level1(self.reagan, self.screen, self.SIZE)
        level_2 = Levels.Level2(self.reagan, self.screen, self.SIZE)

        self.current_level_no = 0
        # TODO: Also add the level objects to this level list
        self.level_list = [level_1, level_2]
        self.current_level = self.level_list[self.current_level_no]
        self.reagan.level = self.current_level



    # TODO: game_loop stuff!
    def game_loop(self):
        exit = False
        while not exit:
            self.clock.tick_busy_loop(60)
            events = self.get_events()
            if self.game_state == "QUIT":
                exit = self.quit_prompt()
            elif self.game_state == "MENU":
                self.display_menu()
            elif self.game_state == "PLAY":
                self.play_level(events)
            elif self.game_state == "PAUSE":
                self.pause_game()
            pygame.display.flip()

    def quit_prompt(self):
        # TODO: Ask the player if they want to quit.
        pygame.quit()
        return True

    # This gets all key inputs, making sure that we always get it all, even if it doesn't matter.
    # All inputs are sent to the object ginput, that can be used to pass information as needed
    def get_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game_state = "QUIT"
            elif event.type == pygame.KEYDOWN:
                # If the player presses escape, we either quit the game or go the pause menu
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "MENU":
                        self.game_state = "QUIT"
                    elif self.game_state == 'PAUSE':
                        self.game_state = 'PLAY'
                    else:
                        self.game_state = "PAUSE"

                # All the other keys:
                elif event.key == pygame.K_RIGHT:
                    self.ginput.right = True
                    self.ginput.right_time = pygame.time.get_ticks()
                elif event.key == pygame.K_LEFT:
                    self.ginput.left = True
                    self.ginput.left_time = pygame.time.get_ticks()
                elif event.key == pygame.K_UP:
                    self.ginput.up = True
                    self.ginput.up_time = pygame.time.get_ticks()
                elif event.key == pygame.K_RETURN:
                    self.ginput.enter = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ginput.right = False
                elif event.key == pygame.K_LEFT:
                    self.ginput.left = False
                elif event.key == pygame.K_UP:
                    self.ginput.up = False
                elif event.key == pygame.K_RETURN:
                    self.ginput.enter = False

    def display_menu(self):
        pass

    def play_level(self, events):
        self.ginput.player_events(self.reagan)
        self.current_level.update()
        countdown_text = self.font.render("Time Remaining: " + str(int(self.current_level.countdown)), 1, (0, 0, 0))
        current_score_text = self.font.render("Level Score: " + str(int(self.current_level.player_score)), 1, (0, 0, 0))
        self.current_level.draw(self.screen)
        self.reagan.update()
        self.reagan.blit_me()
        self.screen.blit(countdown_text, [100, 100])
        self.screen.blit(current_score_text, [100, 130])
        pygame.display.flip()
        self.check_level_state()

    def check_level_state(self):
        if self.reagan.health == 0:
            self.current_level.death_screen(self.screen, self.font, self.clock)
            self.reagan.health = 3
            self.current_level.reset()
            self.reagan.rect.x, self.reagan.rect.y = self.current_level.player_pos
            self.reagan.level = self.current_level
        elif self.current_level.countdown <= 0:
            self.current_level_no += 1
            self.current_level = self.level_list[self.current_level_no]
            self.reagan.level = self.current_level
            self.reagan.rect.x, self.reagan.rect.y = self.current_level.player_pos

    def pause_game(self):
        # TODO: Figure out why this isn't working properly
        if self.ginput.up:
            self.pause_menu.move_up()
        elif self.ginput.down:
            self.pause_menu.move_down()
        elif self.ginput.enter:
            selected = self.pause_menu.select_option()
            self.menu_selected(selected)
        self.pause_menu.render_pause()

    def menu_selected(self, option):
        if option == 'CONTINUE':
            self.game_state = 'PLAY'
        elif option == 'EXIT TO MENU':
            pass # TODO
        elif option == 'EXIT TO DESKTOP':
            pygame.quit()



# This class is just to hold the buttons pressed
class GameInput:
    def __init__(self):
        # The directions/button presses (i.e. self.up, self.down, etc.) tell us what buttons are being pressed
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.enter = False
        # The direction times tell us which has been pressed most recently. This assures that the most recent button
        # press gets priority
        self.left_time = 0
        self.right_time = 0
        self.down_time = 0
        self.up_time = 0

    def player_events(self, player):
        if self.up:
            player.move('J')
            self.up = False
        if self.right and self.right_time > self.left_time:
            player.move('R')
        elif not self.right:
            player.move('RU')
        if self.left and self.left_time > self.right_time:
            player.move('L')
        elif not self.left:
            player.move('LU')

class PauseMenu:
    def __init__(self, display, font, display_size):
        self.selected = 0
        self.options = ['CONTINUE', 'EXIT TO MENU', 'EXIT TO DESKTOP']
        self.WHITE = (0,0,0)
        self.BLUE = (0, 162, 232)
        self.display = display
        self.middle = (display_size[0]/2, display_size[1]/2)
        self.font = font
        self.top = self.get_top()
        # Used to make sure we don't change menu options too quickly
        self.last_change = 0

    def end_menu(self):
        self.selected = 0

    def move_down(self):
        self.selected += 1
        if self.selected > len(self.options):
            self.selected = 0

    def move_up(self):
        self.selected -= 1
        if self.selected < 0:
            self.selected = len(self.options) - 1

    def get_top(self):
        height = 0
        for txt in self.options:
            height += self.font.size(txt)[1]
        return height

    def render_pause(self):
        y = self.middle[1] - self.top/2
        for i in range(len(self.options)):
            option = self.options[i]
            color = ()
            if i == int(self.selected):
                color = self.WHITE
            else:
                color = self.BLUE
            pos = [self.middle[0] - self.font.size(option)[0]/2, y]
            text = self.font.render(option, 1, color)
            self.display.blit(text, pos)
            y += text.get_height()
        pygame.display.flip()

    def select_option(self):
        return self.options[int(self.selected)]


