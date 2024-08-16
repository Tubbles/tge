#!/usr/bin/env python3

class Scheduler:
    def __init__(self):
        self._regular_callbacks = {}

    def register_on(self, schedule, callback):
        if not schedule in self._regular_callbacks:
            self._regular_callbacks[schedule] = []
        self._regular_callbacks[schedule].append(callback)

    def trigger(self, schedule):
        if schedule in self._regular_callbacks:
            for callback in self._regular_callbacks[schedule]:
                callback()
