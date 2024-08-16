#!/usr/bin/env python3

class InputAction:
    """
    This class models all types of actions that can be triggered using human input devices, (eg. keyboard and
    controllers). For example "jump" and "shoot"
    """

    def __init__(self):
        self._callbacks = {}
        self._currently_held = set()

    def register_on_hold(self, action_name, callback):
        action_name += "_hold"
        if not action_name in self._callbacks:
            self._callbacks[action_name] = []
        self._callbacks[action_name].append(callback)

    def register_on_release(self, action_name, callback):
        action_name += "_release"
        if not action_name in self._callbacks:
            self._callbacks[action_name] = []
        self._callbacks[action_name].append(callback)

    def hold(self, action_name):
        self._currently_held.add(action_name)
        action_name += "_hold"
        if action_name in self._callbacks:
            for callback in self._callbacks[action_name]:
                callback()

    def release(self, action_name):
        self._currently_held.remove(action_name)
        action_name += "_release"
        if action_name in self._callbacks:
            for callback in self._callbacks[action_name]:
                callback()

    def get_currently_held(self):
        return self._currently_held


if __name__ == "__main__":
    # TODO : Add tests here
    pass
