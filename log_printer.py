#!/usr/bin/env python3

if __name__ == "__main__":
    from os import environ
    environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "true"
    import pygame
    pygame.init()
    flags = pygame.FULLSCREEN | pygame.NOFRAME
    screen = pygame.display.set_mode((0, 0), flags, vsync=1)
    font = pygame.font.Font(None, 24)
    screen.fill((0, 0, 0))
    with open("log") as file:
        for (line_number, line) in enumerate(file):
            screen.blit(font.render(f"{line.rstrip()}", True, (255, 255, 255)), (0, 20 * line_number))
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and (event.mod == pygame.KMOD_LCTRL or event.mod == pygame.KMOD_RCTRL):
                    running = False

    pygame.quit()
    import sys
    sys.exit()
