#!/usr/bin/env python3

class InputAction:
    """
    This class models all types of actions that can be triggered using human input devices, (eg. keyboard and
    controllers). For example "jump" and "shoot"
    """

    def __init__(self):
        self._callbacks = {}

    def register(self, action_name, callback):
        if not action_name in self._callbacks:
            self._callbacks[action_name] = []
        self._callbacks[action_name].append(callback)

    def trigger(self, action_name):
        if action_name in self._callbacks:
            for callback in self._callbacks["action_name"]:
                callback()


if __name__ == "__main__":
    # TODO : Add tests here
    pass
