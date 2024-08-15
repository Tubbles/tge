#!/usr/bin/env python3

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "true"

import pygame


class Keyboard:
    @classmethod
    def on_key_down(cls, event):
        if event.key == pygame.K_UP:
            on_input(event.key)
        elif event.key == pygame.K_DOWN:
            on_input(event.key)
        elif event.key == pygame.K_LEFT:
            on_input(event.key)
        elif event.key == pygame.K_RIGHT:
            on_input(event.key)
        elif event.key == pygame.K_q and (event.mod == pygame.KMOD_LCTRL or event.mod == pygame.KMOD_RCTRL):
            Game.input_actions["quit"].trigger()
        else:
            print(f"Unknown key down: {event}")

    @classmethod
    def on_key_up(cls, event):
        if event.key == pygame.K_UP:
            on_input_release(event.key)
        elif event.key == pygame.K_DOWN:
            on_input_release(event.key)
        elif event.key == pygame.K_LEFT:
            on_input_release(event.key)
        elif event.key == pygame.K_RIGHT:
            on_input_release(event.key)
