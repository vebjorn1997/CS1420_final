from player import Player, Enemy

def test_player():
    player = Player(0, 0, "P", (255, 255, 0), "Player")
    assert player.x == 0
    assert player.y == 0
    assert player.marker == "P"
    assert player.color == (255, 255, 0)
    assert player.name == "Player"

def test_enemy():
    enemy = Enemy(0, 0, 0, 0, "E", (255, 0, 0), "Enemy", None)
    assert enemy.x == 0
    assert enemy.y == 0
    assert enemy.marker == "E"
    assert enemy.color == (255, 0, 0)
    assert enemy.name == "Enemy"
