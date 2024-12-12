from tile import Tile

def test_tile():
    tile = Tile(0, 0, 0, False, False)
    assert tile.height == 0
    assert tile.temperature == 0
    assert tile.precipitation == 0
    assert tile.forest is False
    assert tile.water is False

def test_calculate_cost():
    tile = Tile(0, 0, 0, False, False)
    tile.calculate_cost()
    assert tile.cost == 1
    tile = Tile(0, 0, 0, True, False)
    tile.calculate_cost()
    assert tile.cost == 2
    tile = Tile(0, 0, 0, False, True)
    tile.calculate_cost()
    assert tile.cost == 0

def add_character():
    tile = Tile(0, 0, 0, False, False)
    tile.add_character("P")
    assert tile.characters == ["P"]
    tile.add_character("E")
    assert tile.characters == ["P", "E"]

def remove_character():
    tile = Tile(0, 0, 0, False, False)
    tile.add_character("P")
    tile.add_character("E")
    tile.remove_character("E")
    assert tile.characters == ["P"]