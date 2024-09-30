import tcod.console
import tcod.context
import tcod.event
import tcod.tileset
import perllin_gen as pn
import player as pl
import random
import numpy as np
# WIDTH, HEIGHT = 100, 100
WIDTH, HEIGHT = 100, 100
VIEW_WIDTH, VIEW_HEIGHT = 90, 50
# VIEW_WIDTH, VIEW_HEIGHT = 50, 30

class Game:
    def __init__(self):
        self.noise_map_height = pn.perlin_noise(WIDTH, HEIGHT)
        self.noise_map_temperature = pn.perlin_noise(WIDTH, HEIGHT)
        self.noise_map_precipitation = pn.perlin_noise(WIDTH, HEIGHT)
        self.world = [[{'height': 0, 'temperature': 0, 'precipitation': 0, 'forest': False, 'water': False} for _ in range(WIDTH)] for _ in range(HEIGHT)]
        for x in range(HEIGHT):
            for y in range(WIDTH):
                self.world[x][y]['height'] = self.noise_map_height[x][y]
                self.world[x][y]['temperature'] = self.noise_map_temperature[x][y]
                self.world[x][y]['precipitation'] = self.noise_map_precipitation[x][y]
                if not self.world[x][y]['forest']:
                    self.world[x][y]['forest'] = self.generate_forest(x, y)
        for _ in range(int(WIDTH*HEIGHT//1000)):
            self.generate_lake(random.randint(3, 8))
    #     self.draw_river(0, 0)

    # def draw_river(self, x, y):
    #     cost = np.ones((WIDTH, HEIGHT), dtype=np.int8, order="F")
    #     graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
    #     pf = tcod.path.Pathfinder(graph)
    #     pf.add_root((0, 0))
    #     path = pf.path_to((50, 50)).tolist()
    #     for x, y in path:
    #         self.world[x][y]['water'] = True



    def draw_world(self, console: tcod.console.Console, view_x: int, view_y: int):
        for x in range(VIEW_WIDTH):
            for y in range(VIEW_HEIGHT):
                world_x = x + view_x
                world_y = y + view_y
                if 0 <= world_x < WIDTH and 0 <= world_y < HEIGHT:
                    height = self.world[world_x][world_y]['height']

                    if height > 0.8: # mountain
                        console.print(x, y, "#")
                    elif height > 0.65: # hill
                        console.print(x, y, "/")
                    elif self.world[world_x][world_y]['water']: # water
                        console.print(x, y, "~", fg=(0, 0, 255))
                    elif self.world[world_x][world_y]['forest']: # forest
                        console.print(x, y, "T", fg=(0, 200, 0))
                    else: # plains
                        console.print(x, y, ".", fg=(0, 255, 0))

    def gen_for(self, x, y):
        for i in range(x-2, x+3):
            for j in range(y-2, y+3):
                if 0 <= i < WIDTH and 0 <= j < HEIGHT:
                    distance = max(abs(i - x), abs(j - y))
                    forest_chance = 0.3 / (distance + 1)
                    if random.random() < forest_chance:
                        self.world[i][j]['forest'] = True
                    if distance <= 1 and random.random() < 0.05:
                        self.gen_for(i, j)

    def generate_forest(self, x, y):
        if self.world[x][y]['height'] > 0.3 and self.world[x][y]['height'] < 0.65:
            if random.random() < 0.05:
                self.gen_for(x, y)
                return True
        return False

    def generate_lake(self, radius: int):
        lake_position = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
        for x in range(lake_position[0] - radius, lake_position[0] + radius):
            for y in range(lake_position[1] - radius, lake_position[1] + radius):
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                    self.generate_lake_tiles(x, y)

    def generate_lake_tiles(self, x, y):
        self.world[x][y]['water'] = True
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if 0 <= i < WIDTH and 0 <= j < HEIGHT:
                    if random.random() < 0.1:
                        self.world[i][j]['water'] = True
                        self.world[i][j]['forest'] = False
                        self.generate_lake_tiles(i, j)

    def get_world(self):
        return print(self.world)


def main() -> None:
    """Script entry point."""
    game = Game()
    player = pl.Player(WIDTH, HEIGHT)
    # Load the font, a 32 by 8 tile font with libtcod's old character layout.
    tileset = tcod.tileset.load_tilesheet(
        "data/dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD,
    )
    console = tcod.console.Console(VIEW_WIDTH, VIEW_HEIGHT, order="F")
    with tcod.context.new(
        columns=console.width, rows=console.height, tileset=tileset,
    ) as context:
        update_needed = True
        while True:
            if update_needed:
                console.clear()

                view_x = max(0, min(player.x - VIEW_WIDTH // 2, WIDTH - VIEW_WIDTH))
                view_y = max(0, min(player.y - VIEW_HEIGHT // 2, HEIGHT - VIEW_HEIGHT))

                game.draw_world(console, view_x, view_y)
                player.draw_player(console, view_x, view_y)
                context.present(console)
                update_needed = False

            for event in tcod.event.wait():
                context.convert_event(event)
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
                elif isinstance(event, tcod.event.KeyDown):
                    if event.sym in [tcod.event.KeySym.w, tcod.event.KeySym.s, tcod.event.KeySym.a, tcod.event.KeySym.d]:
                        if event.sym == tcod.event.KeySym.w:
                            player.move_player(0, -1, game.world)
                        elif event.sym == tcod.event.KeySym.s:
                            player.move_player(0, 1, game.world)
                        elif event.sym == tcod.event.KeySym.a:
                            player.move_player(-1, 0, game.world)
                        elif event.sym == tcod.event.KeySym.d:
                            player.move_player(1, 0, game.world)
                        update_needed = True
                    elif event.sym == tcod.event.KeySym.e:
                        player.change_ground(game.world, player.x, player.y, True)
                        game.gen_for(player.x, player.y)
                    elif event.sym == tcod.event.KeySym.q: # DEBUG
                        print(player.read_world(game, player.x, player.y))


if __name__ == "__main__":
    main()