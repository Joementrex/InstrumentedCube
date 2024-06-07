import pygame
import sys
import time

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# Set up display
screen_size = (500, 500)  # Window size


class VisualPositionAuto:
    def __init__(self, rows, cols, screen_size):
        self.rows = rows
        self.cols = cols
        self.screen_size = screen_size
        self.square_size = screen_size[0] // cols
        self.square_colors = [WHITE] * (rows * cols)
        self.screen = pygame.display.set_mode(screen_size)
        self.running = True

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                index = row * self.cols + col
                color = self.square_colors[index]
                pygame.draw.rect(self.screen, color, (col * self.square_size, row * self.square_size, self.square_size, self.square_size))
                pygame.draw.rect(self.screen, BLACK, (col * self.square_size, row * self.square_size, self.square_size, self.square_size), 1)

    def change_square_color(self, index, color):
        if 0 <= index < self.rows * self.cols:
            self.square_colors[index] = color

    def change_all_square_colors(self, color):
        for i in range(self.rows * self.cols):
            self.square_colors[i] = color

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(WHITE)
            self.draw_grid()
            pygame.display.flip()
            # pygame.time.delay(10)
            time.sleep(0.1)

        pygame.quit()
        sys.exit()

    def stop(self):
        self.running = False

if __name__ == '__main__':
    vis = VisualPositionAuto(5, 5, screen_size)
    vis.change_square_color(12, RED)
    vis.run()
    # Draw a red square in the middle
    