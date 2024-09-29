import tcod.console

class Player:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.x = self.width // 2
        self.y = self.height // 2

    def draw_player(self, console: tcod.console.Console, view_x: int, view_y: int):
        console.print(self.x - view_x, self.y - view_y, "P", fg=(255, 255, 0))  # Yellow color

    def move_player(self, dx: int, dy: int, world):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < self.width and 0 <= new_y < self.height:
            if world[new_x][new_y]['height'] <= 0.8: # stop at height 0.8
                self.x = new_x
                self.y = new_y

    def change_ground(self, world, x, y, value):
        world[x][y]['forest'] = value

    def read_world(self, game, x, y):
        print(f"X: {x}, Y: {y}")
        # print(game.world)
        return game.world[x][y]