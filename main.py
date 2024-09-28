import tcod.console
import tcod.context
import tcod.event
import tcod.tileset
import perllin_gen as pn
import player as pl
import random

# WIDTH, HEIGHT = 100, 100
WIDTH, HEIGHT = 1000, 1000
VIEW_WIDTH, VIEW_HEIGHT = 90, 50
# VIEW_WIDTH, VIEW_HEIGHT = 50, 30

class Game:
    def __init__(self):
        self.noise_map_height = pn.perlin_noise(WIDTH, HEIGHT)
        self.noise_map_temperature = pn.perlin_noise(WIDTH, HEIGHT)
        self.world = [[{'height': 0, 'temperature': 0, 'forest': False, 'water': False} for _ in range(WIDTH)] for _ in range(HEIGHT)]
        for x in range(HEIGHT):
            for y in range(WIDTH):
                self.world[x][y]['height'] = self.noise_map_height[x][y]
                self.world[x][y]['temperature'] = self.noise_map_temperature[x][y]
                # if not self.world[x][y]['forest']:
                self.world[x][y]['forest'] = self.generate_forest(x, y)
                # if not self.world[x][y]['water']:
                self.world[x][y]['water'] = self.generate_water(x, y)

    def draw_world(self, console: tcod.console.Console, view_x: int, view_y: int):
        for x in range(VIEW_WIDTH):
            for y in range(VIEW_HEIGHT):
                world_x = x + view_x
                world_y = y + view_y
                if 0 <= world_x < WIDTH and 0 <= world_y < HEIGHT:
                    height = self.world[world_x][world_y]['height']
                    forest = self.world[world_x][world_y]['forest']
                    water = self.world[world_x][world_y]['water']

                    if height > 0.8: # mountain
                        console.print(x, y, "#")
                    elif height > 0.65: # hill
                        console.print(x, y, "/")
                    elif forest: # forest
                        console.print(x, y, "T", fg=(0, 200, 0))
                    elif water: # water
                        console.print(x, y, "~", fg=(0, 0, 255))
                    else: # plains
                        console.print(x, y, ".", fg=(0, 255, 0))

    def gen_for(self, x, y):
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if 0 <= i < WIDTH and 0 <= j < HEIGHT:
                    if random.random() < 0.1:
                        self.world[i][j]['forest'] = True
                        self.gen_for(i, j)

    def generate_forest(self, x, y):
        if self.world[x][y]['height'] > 0.3 and self.world[x][y]['height'] < 0.65 and self.world[x][y]['temperature'] > 0.3:
            # if random.random() < 0.05:
            # self.gen_for(x, y)
            return True
        return False

    def generate_water(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < WIDTH and 0 <= ny < HEIGHT:
                    if self.world[nx][ny]['height'] < 0.3:
                        return True

        return False

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
                        print(player.read_world(game.world, player.x, player.y))

if __name__ == "__main__":
    main()