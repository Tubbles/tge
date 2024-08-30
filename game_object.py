#!/usr/bin/env python3

import pygame
import sys


class _Game:
    # this class is partially populated by tge
    def loop(self):
        while self.running:
            self.event.pump()
            self.scheduler.trigger("update")
            self.scheduler.trigger("draw")
            pygame.display.flip()
            sys.stdout.flush()
            self.clock.tick(60)  # limits FPS to 60

        # pygame.display.quit()
        pygame.quit()
        # sys.exit(1)


game = _Game()
