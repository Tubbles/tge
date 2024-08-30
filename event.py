#!/usr/bin/env python3

import pygame


class Event:
    def __init__(self):
        self._event_callbacks = {}

    def register_callback(self, event_type, callback):
        if not event_type in self._event_callbacks:
            self._event_callbacks[event_type] = []
        self._event_callbacks[event_type].append(callback)

    def trigger_callbacks(self, event):
        if event.type in self._event_callbacks:
            for cb in self._event_callbacks[event.type]:
                cb(event)
            return True
        return False

    def pump(self):
        for event in pygame.event.get():
            if not self.trigger_callbacks(event):
                print(f"Unknown event: {event}")
