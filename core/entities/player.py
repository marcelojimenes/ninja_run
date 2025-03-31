import pygame
import os

from config.settings import HEIGHT, BLACK
from core.entities.entity import Entity

class Player(Entity):
    def __init__(self, x, y ,width, height, speed, sprite_size):
        self.rect = pygame.Rect((x, y), (width, height))
        self.sprite_size = sprite_size
        self.speed = speed

        self.score = 0
        self.gravity = 1
        self.jump_strength = -15
        self.current_state = ""
        self.current_sprite_index = 0
        self.set_running()

        self.sprites = self.load_sprites("./assets/images/player")
        self.animation_speed = 0.2
        self.image = self.sprites[self.current_state][self.current_sprite_index]

    def load_sprites(self, directory: str):
        states = ["running", "jumping", "game_over"]
        sprites = {}

        for state in states:
            state_dir = os.path.join(directory, state)
            files = sorted([f for f in os.listdir(state_dir) if f.endswith(".png")])

            loaded_sprites = [pygame.image.load(os.path.join(state_dir, file)).convert_alpha() for file in files]
            if self.sprite_size:
                loaded_sprites = [
                    pygame.transform.scale(sprite, self.sprite_size) for sprite in loaded_sprites
                ]

            sprites[state] = loaded_sprites

        return sprites

    def draw(self, screen) -> pygame.Rect:
        self.image = self.sprites[self.current_state][int(self.current_sprite_index)]
        sprite_rect = self.image.get_rect()
        sprite_rect.center = self.rect.midright

        screen.blit(self.image, sprite_rect.topleft)

        # hit box debug
        #pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

        return self.rect

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if self.rect.y >= HEIGHT - 100:
                    self.set_jumping()
                    self.speed = self.jump_strength

    def update(self):
        self.current_sprite_index += self.animation_speed
        if self.current_sprite_index >= len(self.sprites[self.current_state]):
            self.current_sprite_index = 0

        self.speed += self.gravity
        self.rect.y += self.speed

        if self.rect.y >= HEIGHT-100:
            self.rect.y = HEIGHT-100
            self.speed = 0

            if self.current_state == "jumping":
                self.current_state = "running"

    def set_game_over(self):
        # todo - not working as expected
        self.current_state = "game_over"
        self.current_sprite_index = 0

    def set_jumping(self):
        self.current_state = "jumping"
        self.current_sprite_index = 0

    def set_running(self):
        self.current_state = "running"
        self.current_sprite_index = 0

    def increase_score(self):
        self.score += 1

    def get_score(self):
        return self.score
