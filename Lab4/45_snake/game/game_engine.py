import pygame
from .snake import Snake
from .food import Food
from .sounds import Sounds

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.difficulties = {
            "Easy": 6,
            "Medium": 10,
            "Hard": 15,
        }
        self.difficulty_name = "Medium"
        self.moves_per_second = self.difficulties[self.difficulty_name]

        self.game_over = False
        self.quit_requested = False
        self.sounds = Sounds()

        self.score_font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.final_score_font = pygame.font.SysFont("Arial", 30)
        self.quit_font = pygame.font.SysFont("Arial", 24)
        self.difficulty_prompt_font = pygame.font.SysFont("Arial", 24)
        self.difficulty_choice_font = pygame.font.SysFont("Arial", 28, bold=True)
        self.difficulty_hud_font = pygame.font.SysFont("Arial", 18)

        self.reset()

    def reset(self):
        self.snake = Snake(
            self.grid_width // 2,
            self.grid_height // 2,
            self.cell_size
        )
        self.food = Food(
            self.grid_width,
            self.grid_height,
            self.cell_size,
            self.snake.body
        )

        self.score = 0
        self._frame_counter = 0
        self.game_over = False

    def handle_keydown(self, key):
        if self.game_over:
            if key in (pygame.K_ESCAPE, pygame.K_q):
                self.quit_requested = True
            elif key in (pygame.K_1, pygame.K_KP1, pygame.K_e):
                self.start_new_game("Easy")
            elif key in (pygame.K_2, pygame.K_KP2, pygame.K_m):
                self.start_new_game("Medium")
            elif key in (pygame.K_3, pygame.K_KP3, pygame.K_h):
                self.start_new_game("Hard")
            return

        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def handle_input(self):
        # Reserved for continuously-held-key input (not used for a
        # grid-based snake, but kept here to mirror the engine's shape).
        pass

    def end_game(self):
        if self.game_over:
            return

        self.game_over = True
        self.sounds.play_game_over()

    def start_new_game(self, difficulty_name):
        self.difficulty_name = difficulty_name
        self.moves_per_second = self.difficulties[difficulty_name]
        self.reset()

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        self.snake.move()

        if self.snake.collides_with_wall(self.grid_width, self.grid_height):
            self.end_game()
            return

        if self.snake.collides_with_self():
            self.end_game()
            return

        if (
            self.food.x is not None
            and self.food.y is not None
            and self.snake.body[0] == (self.food.x, self.food.y)
        ):
            self.snake.grow()
            self.score += 1
            self.sounds.play_eat()
            self.food.respawn(self.snake.body)

    def _blit_centered(self, screen, text, font, color, y):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.width // 2, y))
        screen.blit(text_surface, text_rect)

    def render(self, screen):
        # Draw food
        pygame.draw.rect(screen, RED, self.food.rect())

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(screen, GREEN, rect)

        # Draw score
        score_text = self.score_font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Draw current difficulty in the top-right corner.
        difficulty_text = self.difficulty_hud_font.render(
            self.difficulty_name,
            True,
            GRAY
        )
        difficulty_rect = difficulty_text.get_rect(
            top=12,
            right=self.width - 10
        )
        screen.blit(difficulty_text, difficulty_rect)

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            self._blit_centered(
                screen,
                "GAME OVER",
                self.game_over_font,
                RED,
                self.height // 2 - 80
            )
            self._blit_centered(
                screen,
                f"Final Score: {self.score}",
                self.final_score_font,
                WHITE,
                self.height // 2
            )
            self._blit_centered(
                screen,
                "Play again - choose difficulty:",
                self.difficulty_prompt_font,
                WHITE,
                self.height // 2 + 48
            )
            self._blit_centered(
                screen,
                "1 Easy    2 Medium    3 Hard",
                self.difficulty_choice_font,
                GREEN,
                self.height // 2 + 88
            )
            self._blit_centered(
                screen,
                "Esc / Q to quit",
                self.quit_font,
                GRAY,
                self.height // 2 + 128
            )
