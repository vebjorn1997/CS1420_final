from abc import ABC, abstractmethod
import tcod.console


class Character(ABC):
    """
    Base class for all characters
    """

    @abstractmethod
    def __init__(self, width: int, height: int, marker: str, color: tuple, name: str):
        self.width = width
        self.height = height
        self.marker = marker
        self.color = color
        self.name = name


class Enemy(Character):
    """
    Enemy class, implements pathfinding to move towards a target (player)
    """

    def __init__(
        self,
        width: int,
        height: int,
        x: int,
        y: int,
        marker: str,
        color: tuple,
        name: str,
        graph: tcod.path.CustomGraph,
    ):
        super().__init__(width, height, marker, color, name)
        self.x = x
        self.y = y
        self.graph = graph

    def move(self, target: "Player"):
        """
        Move the enemy towards the target
        """
        pf = tcod.path.Pathfinder(self.graph)
        pf.add_root((self.x, self.y))
        moves = pf.path_to(target.get_location)
        if len(moves) > 1:
            dx, dy = moves[1]
            if 0 <= dx < self.width and 0 <= dy < self.height:
                self.x = dx
            self.y = dy


class Player(Character):
    """
    Player class, has a method to read the world info for the square the player is on. Can also change the world info for the square the player is on.
    """

    def __init__(self, width: int, height: int, marker: str, color: tuple, name: str):
        super().__init__(width, height, marker, color, name)
        self.x = width // 2
        self.y = height // 2

    @property
    def get_location(self):
        """
        Get the player's location
        """
        return (self.x, self.y)

    def move(self, dx: int, dy: int, world):
        """
        Move the player in the given direction, if the new position is within bounds and height is less than 0.75, move the player
        """
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            if world[new_x][new_y].height <= 0.75:
                self.x = new_x
                self.y = new_y

    def change_ground(self, game, x: int, y: int, value: bool):
        """
        Change the ground type at the given position
        """
        game.world[x][y].forest = value
        game.update_pathfinding_costs()

    def read_world(self, game, x: int, y: int):
        """
        Read the world info at the given position
        """
        print(f"X: {x}, Y: {y}")
        return game.world[x][y]
