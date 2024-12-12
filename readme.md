### Install

- Create a virtual enviorment: 'python -m venv /path/to/new/virtual/environment'
- Activate the virtual enviorment: 'Scripts/activate'
- Then install the requirements: 'pip install -r requirements.txt'
- Run the game: 'python main.py'

## Libraries used:

- tcod - generate the game window and handle input
- noise - generate the terrain
- matplotlib
- numpy

## Controls

- WASD - move
- SPACE - let time pass
- q - debug tool, reads the tile the player is on
- e - generates a forest

## Mechanics

- The object of the game is to stay alive for as long as possible. Time is counted in rounds, where one round is the equvivalent of a move action or a pass action.
- Every 10 rounds, a new enemy spawn.

## Known Bugs

- The enemy is incapable of moving into the water tile.
- Enemies will not spawn in water, this is a feature, because they can't move in water.

## FAQ

- The noise module requires visual studio install which is 7gb. To avoid this install req you can bypass it. First go into the requirements.txt file and remove the noise module. Then run pip install -r requirements.txt.
  Next, got into main.py and comment out line 7, 23, 24, 25, 93, 94, and 95. Then go to tile.py, and change line 10, 11, and 12 to 0.
  This will remove the terrain generation, excpets for water, but the game will still work.
