import tcod.console
import tcod.context
import tcod.event
import tcod.tileset
import perllin_gen as pn
import player as pl

WIDTH, HEIGHT = 1000, 1000
VIEW_WIDTH, VIEW_HEIGHT = 50, 30

class Game:
    def __init__(self):
        self.noise_map_height = pn.perlin_noise(WIDTH, HEIGHT)
        self.noise_map_temperature = pn.perlin_noise(WIDTH, HEIGHT)
        self.world = [[{'height': 0, 'temperature': 0} for _ in range(WIDTH)] for _ in range(HEIGHT)]
        for x in range(HEIGHT):
            for y in range(WIDTH):
                self.world[x][y]['height'] = self.noise_map_height[x][y]
                self.world[x][y]['temperature'] = self.noise_map_temperature[x][y]
        print(self.world[50][50])

    def draw_world(self, console: tcod.console.Console, view_x: int, view_y: int):
        for x in range(VIEW_WIDTH):
            for y in range(VIEW_HEIGHT):
                world_x = x + view_x
                world_y = y + view_y
                if 0 <= world_x < WIDTH and 0 <= world_y < HEIGHT:
                    height = self.world[world_y][world_x]['height']
                    temperature = self.world[world_y][world_x]['temperature']
                    if height > 0.8: # mountain
                        console.print(x, y, "#")
                    elif height > 0.6: # hill
                        console.print(x, y, "/")
                    elif height > 0.2: # lowland
                        if temperature > 0.65:
                            console.print(x, y, "D", fg=(255, 255, 0))  # Desert
                        else:
                            console.print(x, y, ".")  # Plains
                    else:
                        console.print(x, y, "W", fg=(0, 0, 255))  # Water

    def get_world(self):
        return print(self.world)


def main() -> None:
    """Script entry point."""
    game = Game()
    player = pl.Player(WIDTH, HEIGHT)
    # Load the font, a 32 by 8 tile font with libtcod's old character layout.
    tileset = tcod.tileset.load_tilesheet(
        "dejavu16x16_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD,
    )
    console = tcod.console.Console(VIEW_WIDTH, VIEW_HEIGHT, order="F")
    with tcod.context.new(
        columns=console.width, rows=console.height, tileset=tileset,
    ) as context:
        while True:
            console.clear()

            view_x = max(0, min(player.x - VIEW_WIDTH // 2, WIDTH - VIEW_WIDTH))
            view_y = max(0, min(player.y - VIEW_HEIGHT // 2, HEIGHT - VIEW_HEIGHT))


            game.draw_world(console, view_x, view_y)
            player.draw_player(console, view_x, view_y)
            context.present(console)

            for event in tcod.event.wait():
                context.convert_event(event)
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
                elif isinstance(event, tcod.event.KeyDown):
                    if event.sym == tcod.event.K_w:
                        player.move_player(0, -1, game.world)
                    elif event.sym == tcod.event.K_s:
                        player.move_player(0, 1, game.world)
                    elif event.sym == tcod.event.K_a:
                        player.move_player(-1, 0, game.world)
                    elif event.sym == tcod.event.K_d:
                        player.move_player(1, 0, game.world)
                    elif event.sym == tcod.event.K_q:
                        print(player.read_world(game.world, player.x, player.y))

if __name__ == "__main__":
    main()