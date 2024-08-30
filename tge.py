#!/usr/bin/env python3

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "true"

import pygame


pygame.init()


from event import Event
from game_object import game
from input_action import InputAction
from joypad import Joypad
from keyboard import Keyboard
from scheduler import Scheduler


class GameEngine:
    def __init__(self):
        self.game = game
        game.running = True

        # init some pygame stuff
        game.clock = pygame.time.Clock()
        game.screen_flags = pygame.FULLSCREEN | pygame.NOFRAME
        game.screen = pygame.display.set_mode((0, 0), game.screen_flags, vsync=1)

        # init some default systems
        game.joypad = Joypad()
        game.input_action = InputAction()
        game.event = Event()
        game.scheduler = Scheduler()
        game.keyboard = Keyboard()

game_engine = GameEngine()
