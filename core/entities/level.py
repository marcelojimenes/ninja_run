import pygame
import os

from core.entities.entity import Entity


class Level(Entity):
    def __init__(self, directory, screen_width, screen_height):
        self.layers = []
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.load_layers(directory)

    def load_layers(self, directory):
        files = sorted(
            [f for f in os.listdir(directory) if f.endswith(".png")],
        )

        for index, file in enumerate(files):
            full_path = os.path.join(directory, file)
            image = pygame.image.load(full_path)
            image = pygame.transform.scale(image, (self.screen_width, self.screen_height))
            speed = (index + 0.2)

            self.layers.append({"image": image, "x_pos": 0, "speed": speed})

    def update(self):
        for layer in self.layers:
            layer["x_pos"] -= layer["speed"]
            if layer["x_pos"] <= -self.screen_width:
                layer["x_pos"] = 0

    def draw(self, screen):
        for layer in self.layers:
            screen.blit(layer["image"], (layer["x_pos"], 0))
            screen.blit(layer["image"], (layer["x_pos"] + self.screen_width, 0))
