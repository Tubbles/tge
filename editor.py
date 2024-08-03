#!/usr/bin/env python3

import pgzrun
from automata import mapping_from_rule, elementary_cellular_automata

WIDTH = 1000
HEIGHT = 500

class Constants:
    CELLS_WIDTH = 2
    CELLS_HEIGHT = 2
    NUM_CELLS_X = int(WIDTH / CELLS_WIDTH)
    NUM_CELLS_Y = int(HEIGHT / CELLS_HEIGHT)


class Color:
    BLACK = (0, 0, 0)
    DARK_RED = (128, 0, 0)
    WHITE = (255, 255, 255)


class Game:
    trigger_full_redraw = True
    up_counter = 0
    down_counter = 0
    up_pressed = False
    down_pressed = False

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


class Cell:
    def __init__(self):
        self.pos = (0, 0)
        self.active = False
        self.rect = Rect((0, 0), (0, 0))

    def __repr__(self):
        return f"{type(self).__name__}({vars(self)})"


def xy(x, y):
    if x < 0 or y < 0 or x >= Constants.NUM_CELLS_X or y >= Constants.NUM_CELLS_Y:
        raise Exception()
    global cells
    cell = cells[x + y * Constants.NUM_CELLS_X]
    return cell


def init(cells):
    for index, cell in enumerate(cells):
        cell.pos = (index % Constants.NUM_CELLS_X, index // Constants.NUM_CELLS_X)
        left = cell.pos[0] * Constants.CELLS_WIDTH
        top = cell.pos[1] * Constants.CELLS_HEIGHT
        cell.rect.topleft = (left, top)
        cell.rect.size = (Constants.CELLS_WIDTH, Constants.CELLS_HEIGHT)
        cell.active = False


def draw():
    if Game.trigger_full_redraw:
        Game.trigger_full_redraw = False
        global cells
        screen.clear()
        screen.fill(Color.BLACK)
        for cell in cells:
            if cell.active:
                screen.draw.filled_rect(cell.rect, Color.WHITE)

    screen.draw.filled_rect(Rect((0, 0), (80, 20)), Color.BLACK)
    screen.draw.text(f"rule: {Game.get_rule()}", topleft=(0, 0))


def on_key_down(key):
    if key == keys.UP:
        Game.set_rule((Game.get_rule() + 1) % 255)
        Game.up_pressed = True
    elif key == keys.DOWN:
        Game.set_rule((Game.get_rule() - 1) % 255)
        Game.down_pressed = True


def on_key_up(key):
    if key == keys.UP:
        Game.up_pressed = False
    elif key == keys.DOWN:
        Game.down_pressed = False

    if not Game.up_pressed and not Game.down_pressed:
        automate(cells)
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


def automate(cells):
    for cell in cells:
        if cell.pos[1] == 0:
            # Set up the first "seed" row
            if cell.pos[0] == Constants.NUM_CELLS_X // 2:
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


global cells
cells = [Cell() for _ in range(Constants.NUM_CELLS_X * Constants.NUM_CELLS_Y)]
init(cells)
Game.set_rule(110)
automate(cells)
pgzrun.go()
