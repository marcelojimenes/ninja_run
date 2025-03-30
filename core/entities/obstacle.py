import pygame
import random
from config.settings import *
from core.entities.entity import Entity


class Obstacle(Entity):
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def draw(self, surface) -> pygame.Rect:
        return pygame.draw.rect(surface, RED, self.rect)

    def move(self):
        self.rect.x -= self.speed

    def is_off_screen(self):
        return self.rect.x < 0

    def reset_position(self):
        self.rect.x = WIDTH
        self.rect.y = (HEIGHT - 50) - self.rect.height

    def increase_speed(self, increment):
        self.speed += increment
