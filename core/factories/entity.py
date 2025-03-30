from config.settings import HEIGHT
from core.entities.obstacle import Obstacle
from core.entities.player import Player

class EntityFactory:
    @staticmethod
    def create(ent_type, **kwargs) -> Obstacle | Player:
        ground = HEIGHT - 50
        if ent_type == 'obstacle':
            x = kwargs.get('x', 800)
            width = kwargs.get('width', 50)
            height = kwargs.get('height', 50)
            speed = kwargs.get('speed', 5)
            y = ground - height
            return Obstacle(x, y, width, height, speed)

        return Player()
