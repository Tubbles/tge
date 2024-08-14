#!/usr/bin/env python3


class InputAction:
    """
    This class models all types of actions that can be triggered using human input devices, such as keyboard and
    controllers
    """

    def __init__(self, callback=None):
        self._callback = callback  # Callback for the triggered event

    def trigger(self):
        if self._callback:
            self._callback()


if __name__ == "__main__":
    # TODO : Add tests here
    pass
