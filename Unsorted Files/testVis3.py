import multiprocessing
import pygame
import sys

def create_window(color, title):
    pygame.init()
    window_size = (400, 300)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(title)
    screen.fill(color)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    titles = [f"Window {i+1}" for i in range(5)]
    processes = []

    for color, title in zip(colors, titles):
        p = multiprocessing.Process(target=create_window, args=(color, title))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
