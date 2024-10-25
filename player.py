import tcod.console
from abc import ABC, abstractmethod
import random

class Character(ABC):
    @abstractmethod
    def __init__(self, width: int, height: int, marker: str, color: tuple, name: str):
        self.width = width
        self.height = height
        self.marker = marker
        self.color = color
        self.name = name

    @abstractmethod
    def move(self, dx: int, dy: int, world):
        pass

class Enemy(Character):
    def __init__(self, width: int, height: int, x: int, y: int, marker: str, color: tuple, name: str):
        super().__init__(width, height, marker, color, name)
        self.x = x
        self.y = y

    def move(self):
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        direction = random.choices(moves, weights=[0.25, 0.25, 0.25, 0.25])
        dx, dy = direction[0]
        # new_x = self.x + dx
        # new_y = self.y + dy
        # if 0 <= new_x < self.width and 0 <= new_y < self.height:
        #     self.x = new_x
        #     self.y = new_y


class Player(Character):
    def __init__(self, width: int, height: int, marker: str, color: tuple, name: str):
        super().__init__(width, height, marker, color, name)
        self.x = width // 2
        self.y = height // 2

    def move(self, dx: int, dy: int, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            if world[new_x][new_y]['height'] <= 0.75: # stop at height 0.8
                self.x = new_x
                self.y = new_y

    def change_ground(self, world, x, y, value):
        world[x][y]['forest'] = value

    def read_world(self, game, x, y):
        print(f"X: {x}, Y: {y}")
        return game.world[x][y]
