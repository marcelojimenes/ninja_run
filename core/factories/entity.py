from typing import Type
from config.settings import HEIGHT, WIDTH
from core.entities.level import Level
from core.entities.obstacle import Obstacle
from core.entities.player import Player


class EntityFactory:
    @staticmethod
    def create(ent_type, **kwargs) -> Level | Obstacle | Player | Type[NotImplementedError] :
        ground = HEIGHT - 50
        x = kwargs.get('x', 800)
        width = kwargs.get('width', 50)
        height = kwargs.get('height', 50)
        speed = kwargs.get('speed', 5)
        sprite_size = kwargs.get('sprite_size', (60,70))
        y = ground - height

        if ent_type == 'level':
            return Level("assets/images/level", WIDTH, HEIGHT)
        elif ent_type == 'obstacle':
            return Obstacle(x, y, width, height, speed)
        elif ent_type == 'player':
            return Player(x, y, width, height, speed, sprite_size)

        return NotImplementedError
