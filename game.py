# game.py
from game_tools.player import create_player
from game_tools.enemies import create_enemy, enemy_attack

# Now use them to create a simple game scenario
player = create_player("Hero")
enemy = create_enemy("Goblin", 5)

print(f"{player['name']} encounters a {enemy['name']}!")
damage = enemy_attack()
print(f"The {enemy['name']} attacks for {damage} damage!")
player["health"] -= damage
print(f"{player['name']}'s health is now {player['health']}")