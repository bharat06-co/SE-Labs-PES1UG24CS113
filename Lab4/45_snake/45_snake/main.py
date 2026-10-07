import pygame

# Match pygame mixer output to the generated 16-bit mono sounds.
pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
from game.game_engine import GameEngine

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                engine.handle_keydown(event.key)

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        pygame.display.flip()

        if engine.quit_requested:
            running = False
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
