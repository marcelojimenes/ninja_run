import pygame

from config.settings import HEIGHT, BLACK
from core.entities.entity import Entity

class Player(Entity):
    def __init__(self):
        self.rect = pygame.Rect(100, HEIGHT-100, 40, 50)
        self.color = BLACK
        self.score = 0
        self.velocity = 0
        self.gravity = 1
        self.jump_strength = -15

    def draw(self, screen) -> pygame.Rect:
        return pygame.draw.rect(screen, self.color, self.rect)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if self.rect.y >= HEIGHT - 100:
                    self.velocity = self.jump_strength

    def update(self):
        self.velocity += self.gravity
        self.rect.y += self.velocity

        if self.rect.y >= HEIGHT-100:
            self.rect.y = HEIGHT-100
            self.velocity = 0

    def increase_score(self):
        self.score += 1

    def get_score(self):
        return self.score
