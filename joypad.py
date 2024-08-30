#!/usr/bin/env python3

from tge import game, pygame


class Joypad:
    def on_joydevice_added(self, event: pygame.event.Event):
        joy = pygame.joystick.Joystick(event.device_index)
        game.joysticks[joy.get_instance_id()] = joy
        print(f"Joystick {joy.get_instance_id()} connected: {joy.get_name()}")

    def on_joydevice_removed(self, event: pygame.event.Event):
        del game.joysticks[event.instance_id]
        print(f"Joystick {event.instance_id} disconnected")

    def on_joy_button_down(self, event):
        if "microsoft x-box 360" in game.joysticks[event.instance_id].get_name().lower():
            if event.button == 0:  # A Button
                on_input(pygame.K_DOWN)
            elif event.button == 1:  # B Button
                on_input(pygame.K_RIGHT)
            elif event.button == 2:  # X Button
                on_input(pygame.K_LEFT)
            elif event.button == 3:  # Y Button
                on_input(pygame.K_UP)
            elif event.button == 4:  # Left Bumper
                pass
            elif event.button == 5:  # Right Bumper
                pass
            elif event.button == 6:  # Back Button
                game.input_action.hold("quit")
            elif event.button == 7:  # Start Button
                pass
            elif event.button == 8:  # L. Stick In
                pass
            elif event.button == 9:  # R. Stick In
                pass
            elif event.button == 10:  # Guide Button
                pass

    def on_joy_button_up(self, event):
        if "microsoft x-box 360" in game.joysticks[event.instance_id].get_name().lower():
            if event.button == 0:  # A Button
                on_input_release(pygame.K_DOWN)
            elif event.button == 1:  # B Button
                on_input_release(pygame.K_RIGHT)
            elif event.button == 2:  # X Button
                on_input_release(pygame.K_LEFT)
            elif event.button == 3:  # Y Button
                on_input_release(pygame.K_UP)
            elif event.button == 4:  # Left Bumper
                pass
            elif event.button == 5:  # Right Bumper
                pass
            elif event.button == 6:  # Back Button
                pass
            elif event.button == 7:  # Start Button
                pass
            elif event.button == 8:  # L. Stick In
                pass
            elif event.button == 9:  # R. Stick In
                pass
            elif event.button == 10:  # Guide Button
                pass

    def on_joy_axis_motion(self, event):
        pass
