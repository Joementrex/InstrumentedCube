import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_size = (500, 500)  # Window size
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('25 Squares Grid')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Grid settings
rows = 5
cols = 5
square_size = screen_size[0] // cols

# Create a list to store the colors of each square
square_colors = [WHITE] * (rows * cols)

def draw_grid():
    for row in range(rows):
        for col in range(cols):
            index = row * cols + col
            color = square_colors[index]
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))
            pygame.draw.rect(screen, BLACK, (col * square_size, row * square_size, square_size, square_size), 1)

def change_square_color(index, color):
    if 0 <= index < rows * cols:
        square_colors[index] = color

def change_all_square_colors(color):
    for i in range(rows * cols):
        square_colors[i] = color

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Example usage: Change color of squares in order
    for i in range(25):
        change_all_square_colors(WHITE)
        change_square_color(i, RED)
        screen.fill(WHITE)
        draw_grid()
        pygame.display.flip()
        pygame.time.delay(200)  # Wait for 200 milliseconds

    running = False  # Exit after one pass

# Quit Pygame
pygame.quit()
sys.exit()
