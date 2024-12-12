class Tile:
    """
    Holds the properties of a tile. Used to generate the map and for pathfinding.
    """
    def __init__(
        self,
        height: int,
        temperature: int,
        precipitation: int,
        forest: bool,
        water: bool,
    ):
        self.height = height
        self.temperature = temperature
        self.precipitation = precipitation
        self.forest = forest
        self.water = water
        self.characters: list[str] = []
        self.cost: int = 1

    def calculate_cost(self):
        """
        Calculate the cost of the tile, cost is used for pathfinding
        """
        if self.water:
            self.cost = 0
        elif self.forest:
            self.cost = 2
        elif self.height > 0.65:
            self.cost = 5
        else:
            self.cost = 1

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height: int):
        self._height = height

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, temperature: int):
        self._temperature = temperature

    @property
    def precipitation(self):
        return self._precipitation

    @precipitation.setter
    def precipitation(self, precipitation: int):
        self._precipitation = precipitation

    @property
    def forest(self):
        return self._forest

    @forest.setter
    def forest(self, forest: bool):
        self._forest = forest

    @property
    def water(self):
        return self._water

    @water.setter
    def water(self, water: bool):
        self._water = water

    def add_character(self, character: str):
        self.characters.append(character)

    def remove_character(self, character: str):
        self.characters = [c for c in self.characters if c != character]

    def __str__(self):
        return f"Tile(cost={self.cost}, height={self.height}, temperature={self.temperature}, precipitation={self.precipitation}, forest={self.forest}, water={self.water}, characters={self.characters})"
