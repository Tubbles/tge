#!/usr/bin/env python3

from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "true"

import pygame


pygame.init()


from game import Game
import sys


if __name__ == "__main__":
    game = Game()
    game.set_rule(110)
    game.automate()

    game.input_action.register_on_hold("quit", game.quit)
    game.input_action.register_on_hold("next_rule", game.next_rule_hold)
    game.input_action.register_on_release("next_rule", game.next_rule_release)
    game.input_action.register_on_hold("prev_rule", game.prev_rule_hold)
    game.input_action.register_on_release("prev_rule", game.prev_rule_release)
    game.input_action.register_on_hold("inc_size", game.inc_size_hold)
    game.input_action.register_on_release("inc_size", game.inc_size_release)
    game.input_action.register_on_hold("dec_size", game.dec_size_hold)
    game.input_action.register_on_release("dec_size", game.dec_size_release)

    game.event.register_callback(pygame.QUIT, lambda: game.input_action.trigger("quit"))
    game.event.register_callback(pygame.ACTIVEEVENT, game.on_gain_focus)
    game.event.register_callback(pygame.KEYDOWN, game.keyboard.on_key_down)
    game.event.register_callback(pygame.KEYUP, game.keyboard.on_key_up)
    game.event.register_callback(pygame.JOYDEVICEADDED, game.joypad.on_joydevice_added)
    game.event.register_callback(pygame.JOYDEVICEREMOVED, game.joypad.on_joydevice_removed)
    game.event.register_callback(pygame.JOYBUTTONDOWN, game.joypad.on_joy_button_down)
    game.event.register_callback(pygame.JOYBUTTONUP, game.joypad.on_joy_button_up)
    game.event.register_callback(pygame.JOYAXISMOTION, game.joypad.on_joy_axis_motion)

    game.scheduler.register_on("update", game.update)
    game.scheduler.register_on("draw", game.draw)

    while game.running:
        game.event.pump()
        game.scheduler.trigger("update")
        game.scheduler.trigger("draw")
        pygame.display.flip()
        sys.stdout.flush()
        game.clock.tick(60)  # limits FPS to 60

    # pygame.display.quit()
    pygame.quit()
    # sys.exit(1)
