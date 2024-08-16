#!/usr/bin/env python3

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "true"

import pygame


class Keyboard:
    def __init__(self, game):
        self.game = game

    def on_key_down(self, event):
        if event.key == pygame.K_UP:
            self.game.input_action.hold("next_rule")
        elif event.key == pygame.K_DOWN:
            self.game.input_action.hold("prev_rule")
        elif event.key == pygame.K_LEFT:
            self.game.input_action.hold("dec_size")
        elif event.key == pygame.K_RIGHT:
            self.game.input_action.hold("inc_size")
        elif event.key == pygame.K_q and (event.mod == pygame.KMOD_LCTRL or event.mod == pygame.KMOD_RCTRL):
            self.game.input_action.hold("quit")
        else:
            print(f"Unknown key down: {event}")

    def on_key_up(self, event):
        if event.key == pygame.K_UP:
            self.game.input_action.release("next_rule")
        elif event.key == pygame.K_DOWN:
            self.game.input_action.release("prev_rule")
        elif event.key == pygame.K_LEFT:
            self.game.input_action.release("dec_size")
        elif event.key == pygame.K_RIGHT:
            self.game.input_action.release("inc_size")
