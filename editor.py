#!/usr/bin/env python3

import pygame
from automata import mapping_from_rule, elementary_cellular_automata
import math
import sys


pygame.init()


class Color:
    BLACK = (0, 0, 0)
    DARK_RED = (128, 0, 0)
    WHITE = (255, 255, 255)


class Cell:
    def __init__(self):
        self.pos = (0, 0)
        self.active = False
        self.rect = pygame.Rect((0, 0), (0, 0))

    def __repr__(self):
        return f"{type(self).__name__}({vars(self)})"


class Game:
    trigger_full_redraw = True
    up_counter = 0
    down_counter = 0
    up_pressed = False
    down_pressed = False
    running = True
    font = pygame.font.Font(None, 24)
    clock = pygame.time.Clock()
    flags = pygame.FULLSCREEN | pygame.NOFRAME
    screen = pygame.display.set_mode((0, 0), flags, vsync=1)
    WIDTH = screen.get_size()[0]
    HEIGHT = screen.get_size()[1]
    CELLS_WIDTH = 8
    CELLS_HEIGHT = 8
    NUM_CELLS_X = WIDTH // CELLS_WIDTH
    NUM_CELLS_Y = HEIGHT // CELLS_HEIGHT
    cells = [Cell() for _ in range(NUM_CELLS_X * NUM_CELLS_Y)]

    @classmethod
    def init(cls):
        """ Run once during start of the game
        """
        cls.trigger_full_redraw = True
        cls.up_counter = 0
        cls.down_counter = 0
        cls.up_pressed = False
        cls.down_pressed = False
        cls.running = True
        cls.clock = pygame.time.Clock()
        cls.flags = pygame.FULLSCREEN | pygame.NOFRAME
        cls.screen = pygame.display.set_mode((0, 0), cls.flags, vsync=1)
        cls.font = pygame.font.Font(None, 24)
        cls.WIDTH = cls.screen.get_size()[0]
        cls.HEIGHT = cls.screen.get_size()[1]
        cls.CELLS_WIDTH = 8
        cls.CELLS_HEIGHT = 8
        cls.init_cells()

    @classmethod
    def init_cells(cls):
        """ Run once every time the game changes settings
        """
        cls.NUM_CELLS_X = cls.WIDTH // cls.CELLS_WIDTH
        cls.NUM_CELLS_Y = cls.HEIGHT // cls.CELLS_HEIGHT
        cls.cells = [Cell() for _ in range(cls.NUM_CELLS_X * cls.NUM_CELLS_Y)]

        for index, cell in enumerate(cls.cells):
            cell.pos = (index % cls.NUM_CELLS_X, index // cls.NUM_CELLS_X)
            left = cell.pos[0] * cls.CELLS_WIDTH
            top = cell.pos[1] * cls.CELLS_HEIGHT
            cell.rect.topleft = (left, top)
            cell.rect.size = (cls.CELLS_WIDTH, cls.CELLS_HEIGHT)
            cell.active = False
        pass

    @classmethod
    def automate(cls):
        for cell in cls.cells:
            if cell.pos[1] == 0:
                # Set up the first "seed" row
                if cell.pos[0] == Game.NUM_CELLS_X // 2:
                    cell.active = True
                else:
                    cell.active = False
            else:
                prev_cells = [False, False, False]
                try:
                    prev_cells[0] = xy(cell.pos[0] - 1, cell.pos[1] - 1).active
                except Exception:
                    pass
                try:
                    prev_cells[1] = xy(cell.pos[0] + 0, cell.pos[1] - 1).active
                except Exception:
                    pass
                try:
                    prev_cells[2] = xy(cell.pos[0] + 1, cell.pos[1] - 1).active
                except Exception:
                    pass

                cell.active = elementary_cellular_automata(prev_cells, Game.get_rule_mapping())


    @classmethod
    def set_rule(cls, rule):
        cls._rule = rule
        cls._rule_mapping = mapping_from_rule(rule)

    @classmethod
    def get_rule(cls):
        return cls._rule

    @classmethod
    def get_rule_mapping(cls):
        return cls._rule_mapping


def xy(x, y):
    if x < 0 or y < 0 or x >= Game.NUM_CELLS_X or y >= Game.NUM_CELLS_Y:
        raise Exception()
    cell = Game.cells[x + y * Game.NUM_CELLS_X]
    return cell


def draw():
    if Game.trigger_full_redraw:
        Game.trigger_full_redraw = False
        Game.screen.fill(Color.BLACK)
        for cell in Game.cells:
            if cell.active:
                pygame.draw.rect(Game.screen, Color.WHITE, cell.rect)

    pygame.draw.rect(Game.screen, Color.BLACK, pygame.Rect((0, 0), (140, 20*4)))
    Game.screen.blit(Game.font.render(f"res: {Game.screen.get_size()}", True, Color.WHITE), (0, 0))
    Game.screen.blit(Game.font.render(f"side: {Game.CELLS_HEIGHT}", True, Color.WHITE), (0, 20))
    Game.screen.blit(Game.font.render(f"rule: {Game.get_rule()}", True, Color.WHITE), (0, 40))
    Game.screen.blit(Game.font.render(f"fps: {Game.clock.get_fps():.2f}", True, Color.WHITE), (0, 60))


def on_key_down(event):
    if event.key == pygame.K_UP:
        Game.set_rule((Game.get_rule() + 1) % 255)
        Game.up_pressed = True
    elif event.key == pygame.K_DOWN:
        Game.set_rule((Game.get_rule() - 1) % 255)
        Game.down_pressed = True
    elif event.key == pygame.K_LEFT:
        Game.CELLS_WIDTH = min(max(1, math.floor(Game.CELLS_WIDTH * 0.8888889)), 250)
        Game.CELLS_HEIGHT = min(max(1, math.floor(Game.CELLS_HEIGHT * 0.8888889)), 250)
        Game.init_cells()
    elif event.key == pygame.K_RIGHT:
        Game.CELLS_WIDTH = min(max(1, math.ceil(Game.CELLS_WIDTH * 1.125)), 250)
        Game.CELLS_HEIGHT = min(max(1, math.ceil(Game.CELLS_HEIGHT * 1.125)), 250)
        Game.init_cells()
    elif event.key == pygame.K_q and (event.mod == pygame.KMOD_LCTRL or event.mod == pygame.KMOD_RCTRL):
        Game.running = False
    else:
        print(f"Unknown key down: {event}")


def on_key_up(event):
    if event.key == pygame.K_UP:
        Game.up_pressed = False
    elif event.key == pygame.K_DOWN:
        Game.down_pressed = False

    if not Game.up_pressed and not Game.down_pressed:
        Game.automate()
        Game.trigger_full_redraw = True


def update():
    if Game.up_pressed:
        Game.up_counter += 1
    else:
        Game.up_counter = 0

    if Game.down_pressed:
        Game.down_counter += 1
    else:
        Game.down_counter = 0

    if Game.up_counter >= 10:
        Game.set_rule((Game.get_rule() + 1) % 255)
    if Game.down_counter >= 10:
        Game.set_rule((Game.get_rule() - 1) % 255)


Game.init()
Game.set_rule(110)
Game.automate()

joysticks = {}

while Game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Game.running = False
        elif event.type == pygame.KEYDOWN:
            on_key_down(event)
        elif event.type == pygame.KEYUP:
            on_key_up(event)
        elif event.type == pygame.ACTIVEEVENT:
            if event.state == "SDL_APPACTIVE" and event.gain == 1:
                Game.trigger_full_redraw = True
        # Handle hotplugging
        elif event.type == pygame.JOYDEVICEADDED:
            # This event will be generated when the program starts for every
            # joystick, filling up the list without needing to create them manually.
            joy = pygame.joystick.Joystick(event.device_index)
            #joy.init()
            joysticks[joy.get_instance_id()] = joy
            print(f"Joystick {joy.get_instance_id()} connencted")
        elif event.type == pygame.JOYDEVICEREMOVED:
            #joysticks[event.instance_id].quit()
            del joysticks[event.instance_id]
            print(f"Joystick {event.instance_id} disconnected")
        else:
            print(f"Unknown event: {event}")


    update()
    draw()
    pygame.display.flip()

    sys.stdout.flush()
    Game.clock.tick(60)  # limits FPS to 60

pygame.quit()
