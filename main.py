import sys
import random
import tcod.console
import tcod.context
import tcod.event
import tcod.tileset
import perlin_gen as pn
import player as pl
import numpy as np
from tile import Tile

WIDTH, HEIGHT = 100, 100
VIEW_WIDTH, VIEW_HEIGHT = 90, 50


class WorldGenerator:
    """
    World generator class, generates the world and the graph for pathfinding
    """

    def __init__(self):
        self.rounds = 0
        self.noise_map_height = pn.perlin_noise(WIDTH, HEIGHT)
        self.noise_map_temperature = pn.perlin_noise(WIDTH, HEIGHT)
        self.noise_map_precipitation = pn.perlin_noise(WIDTH, HEIGHT)
        self.world = [
            [Tile(0, 0, 0, False, False) for _ in range(WIDTH)] for _ in range(HEIGHT)
        ]
        cost = np.array(
            [[self.world[x][y].cost for y in range(HEIGHT)] for x in range(WIDTH)],
            dtype=np.int8,
        )
        self.graph = tcod.path.SimpleGraph(cost=cost, cardinal=1, diagonal=1)

    def update_pathfinding_costs(self):
        for x in range(WIDTH):
            for y in range(HEIGHT):
                self.world[x][y].calculate_cost()
        cost = np.array(
            [[self.world[x][y].cost for y in range(HEIGHT)] for x in range(WIDTH)],
            dtype=np.int8,
        )
        self.graph = tcod.path.SimpleGraph(cost=cost, cardinal=1, diagonal=2)

    def gen_for(self, x, y):
        for i in range(x - 2, x + 3):
            for j in range(y - 2, y + 3):
                if 0 <= i < WIDTH and 0 <= j < HEIGHT:
                    distance = max(abs(i - x), abs(j - y))
                    forest_chance = 0.3 / (distance + 1)
                    if random.random() < forest_chance:
                        self.world[i][j].forest = True
                    if distance <= 1 and random.random() < 0.05:
                        self.gen_for(i, j)

    def generate_forest(self, x, y):
        if self.world[x][y].height > 0.3 and self.world[x][y].height < 0.65:
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
        self.world[x][y].water = True
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if 0 <= i < WIDTH and 0 <= j < HEIGHT:
                    if random.random() < 0.1:
                        self.world[i][j].water = True
                        self.world[i][j].forest = False
                        self.generate_lake_tiles(i, j)

    def round_end(self):
        self.rounds += 1


class Game(WorldGenerator):
    """
    Game class, handles drawing the world and characters, and checking if the player is dead
    """

    def __init__(self):
        super().__init__()
        for x in range(HEIGHT):
            for y in range(WIDTH):
                self.world[x][y].height = self.noise_map_height[x][y]
                self.world[x][y].temperature = self.noise_map_temperature[x][y]
                self.world[x][y].precipitation = self.noise_map_precipitation[x][y]
                if not self.world[x][y].forest:
                    self.world[x][y].forest = self.generate_forest(x, y)
        for _ in range(int(WIDTH * HEIGHT // 1000)):
            self.generate_lake(random.randint(3, 8))
        self.update_pathfinding_costs()
        self.enemies: list[pl.Enemy] = []

    def draw_world(self, console: tcod.console.Console, view_x: int, view_y: int):
        """
        Draw the visible part of the world to the console
        """
        for x in range(VIEW_WIDTH):
            for y in range(VIEW_HEIGHT):
                world_x = x + view_x
                world_y = y + view_y
                if 0 <= world_x < WIDTH and 0 <= world_y < HEIGHT:
                    height = self.world[world_x][world_y].height

                    if height > 0.75:  # mountain
                        console.print(x, y, "#")
                    elif height > 0.65:  # hill
                        console.print(x, y, "/")
                    elif self.world[world_x][world_y].water:  # water
                        console.print(x, y, "~", fg=(0, 0, 255))
                    elif self.world[world_x][world_y].forest:  # forest
                        console.print(x, y, "T", fg=(0, 200, 0))
                    else:  # plains
                        console.print(x, y, ".", fg=(0, 255, 0))

    def draw_character(
        self,
        console: tcod.console.Console,
        view_x: int,
        view_y: int,
        character: pl.Character,
    ):
        """
        Draw the character on the console, and update the list of characters in the tile
        """
        console.print(
            character.x - view_x,
            character.y - view_y,
            character.marker,
            fg=character.color,
        )
        # remove all characters from the list if the name matches, and append the new one
        self.world[character.x][character.y].remove_character(character.name)
        self.world[character.x][character.y].add_character(character.name)

    def check_game_over(self, character: pl.Character):
        """
        Check if the player tile has an enemy on it, if so, game over
        """
        if "Enemy" in self.world[character.x][character.y].characters:
            print(f"{character.name} has died")
            print(f"Game Over! You lasted {self.rounds} rounds")
            sys.exit()

    def spawn_enemy(self, player: pl.Player):
        """
        Spawn an enemy at a random position around the player, if the position is water, don't spawn an enemy
        """
        x = player.x + (
            random.randint(5, 10) if random.random() > 0.5 else random.randint(-10, -5)
        )
        y = player.y + (
            random.randint(5, 10) if random.random() > 0.5 else random.randint(-10, -5)
        )

        if self.world[x][y].water:
            return

        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            self.enemies.append(
                pl.Enemy(WIDTH, HEIGHT, x, y, "E", (255, 0, 0), "Enemy", self.graph)
            )


def main() -> None:
    game = Game()
    player = pl.Player(WIDTH, HEIGHT, "P", (255, 255, 0), "Player")
    game.spawn_enemy(player)

    tileset = tcod.tileset.load_tilesheet(
        "data/dejavu16x16_gs_tc.png",
        32,
        8,
        tcod.tileset.CHARMAP_TCOD,
    )
    console = tcod.console.Console(VIEW_WIDTH, VIEW_HEIGHT, order="F")
    with tcod.context.new(
        columns=console.width,
        rows=console.height,
        tileset=tileset,
    ) as context:
        update_needed = True
        while True:
            if update_needed:
                game.round_end()
                if game.rounds % 10 == 0:
                    game.spawn_enemy(player)
                console.clear()

                # Calculate view position
                view_x = max(0, min(player.x - VIEW_WIDTH // 2, WIDTH - VIEW_WIDTH))
                view_y = max(0, min(player.y - VIEW_HEIGHT // 2, HEIGHT - VIEW_HEIGHT))

                game.draw_world(console, view_x, view_y)

                # Draw characters - player and enemy(s)
                game.draw_character(console, view_x, view_y, player)
                for enemy in game.enemies:
                    game.draw_character(console, view_x, view_y, enemy)

                # Check if player is dead
                game.check_game_over(player)

                # Move enemy(s) on update
                for enemy in game.enemies:
                    enemy.move(player)

                context.present(console)
                update_needed = False

            for event in tcod.event.wait():
                context.convert_event(event)
                if isinstance(event, tcod.event.Quit):
                    raise SystemExit()
                elif isinstance(event, tcod.event.KeyDown):
                    if event.sym in [
                        tcod.event.KeySym.w,
                        tcod.event.KeySym.s,
                        tcod.event.KeySym.a,
                        tcod.event.KeySym.d,
                        tcod.event.KeySym.SPACE,
                    ]:
                        if event.sym == tcod.event.KeySym.w:
                            player.move(0, -1, game.world)
                        elif event.sym == tcod.event.KeySym.s:
                            player.move(0, 1, game.world)
                        elif event.sym == tcod.event.KeySym.a:
                            player.move(-1, 0, game.world)
                        elif event.sym == tcod.event.KeySym.d:
                            player.move(1, 0, game.world)
                        elif event.sym == tcod.event.KeySym.SPACE:
                            pass
                        update_needed = True
                    elif event.sym == tcod.event.KeySym.e:
                        player.change_ground(game, player.x, player.y, True)
                        game.gen_for(player.x, player.y)
                    elif event.sym == tcod.event.KeySym.q:  # DEBUG
                        print(player.read_world(game, player.x, player.y))


if __name__ == "__main__":
    main()
