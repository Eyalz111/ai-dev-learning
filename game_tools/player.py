# game_tools/player.py
def create_player(name):
    return {"name": name, "health": 100, "score": 0}

def heal_player(player, amount):
    player["health"] += amount
    return player

if __name__ == "__main__":
    # Test create_player
    test_player = create_player("Test Hero")
    print("Initial player:", test_player)

    # Test heal_player
    healed_player = heal_player(test_player, 25)
    print("After healing:", healed_player)