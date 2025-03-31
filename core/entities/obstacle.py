import pygame
from config.settings import *
from core.entities.entity import Entity


class Obstacle(Entity):
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect((x, y), (width, height))
        self.image = pygame.image.load("./assets/images/obstacles/rock.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.speed = speed


    def draw(self, screen) -> pygame.Rect:
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # hit box debug
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        return self.rect


    def move(self):
        self.rect.x -= self.speed

    def is_off_screen(self):
        return self.rect.x < 0

    def reset_position(self):
        self.rect.x = WIDTH
        self.rect.y = (HEIGHT - 50) - self.rect.height

    def increase_speed(self, increment):
        self.speed += increment
