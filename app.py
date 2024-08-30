#!/usr/bin/env python3

from tge import game, pygame
from automata import mapping_from_rule, elementary_cellular_automata
from constants import Color
import math
import sys


def get_version():
    version = "0.1.0"

    try:
        import git
        try:
            repo = git.Repo(search_parent_directories=False)
            sha = repo.head.object.hexsha
            version += f"-{sha[0:7]}"
        except git.exc.InvalidGitRepositoryError:
            pass
    except ModuleNotFoundError:
        pass

    return version


class Cell:
    def __init__(self):
        self.pos = (0, 0)
        self.active = False
        self.rect = pygame.Rect((0, 0), (0, 0))

    def __repr__(self):
        return f"{type(self).__name__}({vars(self)})"


class App:
    def __init__(self):
        self.version = get_version()
        self.trigger_full_redraw = True
        self.up_counter = 0
        self.down_counter = 0
        self.up_pressed = False
        self.down_pressed = False
        self.font = pygame.font.Font(None, 24)
        self.WIDTH = game.screen.get_size()[0]
        self.HEIGHT = game.screen.get_size()[1]
        self.CELLS_WIDTH = 8
        self.CELLS_HEIGHT = 8
        self.joysticks = {}
        self.init_cells()
        self.set_rule(110)
        self.automate()

        game.input_action.register_on_hold("quit", self.quit)
        game.input_action.register_on_hold("next_rule", self.next_rule_hold)
        game.input_action.register_on_release("next_rule", self.next_rule_release)
        game.input_action.register_on_hold("prev_rule", self.prev_rule_hold)
        game.input_action.register_on_release("prev_rule", self.prev_rule_release)
        game.input_action.register_on_hold("inc_size", self.inc_size_hold)
        game.input_action.register_on_release("inc_size", self.inc_size_release)
        game.input_action.register_on_hold("dec_size", self.dec_size_hold)
        game.input_action.register_on_release("dec_size", self.dec_size_release)

        game.event.register_callback(pygame.QUIT, lambda: game.input_action.trigger("quit"))
        game.event.register_callback(pygame.ACTIVEEVENT, self.on_gain_focus)
        game.event.register_callback(pygame.KEYDOWN, game.keyboard.on_key_down)
        game.event.register_callback(pygame.KEYUP, game.keyboard.on_key_up)
        game.event.register_callback(pygame.JOYDEVICEADDED, game.joypad.on_joydevice_added)
        game.event.register_callback(pygame.JOYDEVICEREMOVED, game.joypad.on_joydevice_removed)
        game.event.register_callback(pygame.JOYBUTTONDOWN, game.joypad.on_joy_button_down)
        game.event.register_callback(pygame.JOYBUTTONUP, game.joypad.on_joy_button_up)
        game.event.register_callback(pygame.JOYAXISMOTION, game.joypad.on_joy_axis_motion)

        game.scheduler.register_on("update", self.update)
        game.scheduler.register_on("draw", self.draw)


    def init_cells(self):
        """ Run once every time the game changes settings
        """
        self.NUM_CELLS_X = self.WIDTH // self.CELLS_WIDTH
        self.NUM_CELLS_Y = self.HEIGHT // self.CELLS_HEIGHT
        self.cells = [Cell() for _ in range(self.NUM_CELLS_X * self.NUM_CELLS_Y)]

        for index, cell in enumerate(self.cells):
            cell.pos = (index % self.NUM_CELLS_X, index // self.NUM_CELLS_X)
            left = cell.pos[0] * self.CELLS_WIDTH
            top = cell.pos[1] * self.CELLS_HEIGHT
            cell.rect.topleft = (left, top)
            cell.rect.size = (self.CELLS_WIDTH, self.CELLS_HEIGHT)
            cell.active = False

    def automate(self):
        rule_mapping = self.get_rule_mapping()
        for cell in self.cells:
            if cell.pos[1] == 0:
                # Set up the first "seed" row
                if cell.pos[0] == self.NUM_CELLS_X // 2:
                    cell.active = True
                else:
                    cell.active = False
            else:
                prev_cells = [False, False, False]
                try:
                    prev_cells[0] = self.xy(cell.pos[0] - 1, cell.pos[1] - 1).active
                except Exception:
                    pass
                try:
                    prev_cells[1] = self.xy(cell.pos[0] + 0, cell.pos[1] - 1).active
                except Exception:
                    pass
                try:
                    prev_cells[2] = self.xy(cell.pos[0] + 1, cell.pos[1] - 1).active
                except Exception:
                    pass

                cell.active = elementary_cellular_automata(prev_cells, rule_mapping)
                pass


    def set_rule(self, rule):
        self._rule = rule
        self._rule_mapping = mapping_from_rule(rule)

    def get_rule(self):
        return self._rule

    def get_rule_mapping(self):
        return self._rule_mapping

    def xy(self, x, y):
        if x < 0 or y < 0 or x >= self.NUM_CELLS_X or y >= self.NUM_CELLS_Y:
            raise Exception()
        cell = self.cells[x + y * self.NUM_CELLS_X]
        return cell

    def draw(self):
        if self.trigger_full_redraw:
            self.trigger_full_redraw = False
            game.screen.fill(Color.BLACK)
            for cell in self.cells:
                if cell.active:
                    pygame.draw.rect(game.screen, Color.WHITE, cell.rect)

        pygame.draw.rect(game.screen, Color.BLACK, pygame.Rect((0, 0), (160, 20*5)))
        game.screen.blit(self.font.render(f"ver: {self.version}", True, Color.WHITE), (0, 0))
        game.screen.blit(self.font.render(f"res: {game.screen.get_size()}", True, Color.WHITE), (0, 20))
        game.screen.blit(self.font.render(f"side: {self.CELLS_HEIGHT}", True, Color.WHITE), (0, 40))
        game.screen.blit(self.font.render(f"rule: {self.get_rule()}", True, Color.WHITE), (0, 60))
        game.screen.blit(self.font.render(f"fps: {game.clock.get_fps():.2f}", True, Color.WHITE), (0, 80))

    def update(self):
        if self.up_pressed:
            self.up_counter += 1
        else:
            self.up_counter = 0

        if self.down_pressed:
            self.down_counter += 1
        else:
            self.down_counter = 0

        if self.up_counter >= 10:
            self.set_rule((self.get_rule() + 1) % 255)
        if self.down_counter >= 10:
            self.set_rule((self.get_rule() - 1) % 255)

    def quit(self):
        game.running = False

    def on_gain_focus(self, event):
        if event.state == "SDL_APPACTIVE" and event.gain == 1:
            self.trigger_full_redraw = True

    def next_rule_hold(self):
        self.set_rule((self.get_rule() + 1) % 255)
        self.up_pressed = True

    def next_rule_release(self):
        self.up_pressed = False
        if not self.up_pressed and not self.down_pressed:
            self.automate()
            self.trigger_full_redraw = True

    def prev_rule_hold(self):
        self.set_rule((self.get_rule() - 1) % 255)
        self.down_pressed = True

    def prev_rule_release(self):
        self.down_pressed = False
        if not self.up_pressed and not self.down_pressed:
            self.automate()
            self.trigger_full_redraw = True
    def inc_size_hold(self):
        self.CELLS_WIDTH = min(max(1, math.ceil(self.CELLS_WIDTH * 1.125)), 250)
        self.CELLS_HEIGHT = min(max(1, math.ceil(self.CELLS_HEIGHT * 1.125)), 250)
        self.init_cells()

    def inc_size_release(self):
        if not self.up_pressed and not self.down_pressed:
            self.automate()
            self.trigger_full_redraw = True

    def dec_size_hold(self):
        self.CELLS_WIDTH = min(max(1, math.floor(self.CELLS_WIDTH * 0.8888889)), 250)
        self.CELLS_HEIGHT = min(max(1, math.floor(self.CELLS_HEIGHT * 0.8888889)), 250)
        self.init_cells()

    def dec_size_release(self):
        if not self.up_pressed and not self.down_pressed:
            self.automate()
            self.trigger_full_redraw = True
