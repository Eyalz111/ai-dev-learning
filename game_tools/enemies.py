import random

def create_enemy(name, damage):
    """Creates an enemy with the given name and damage"""
    return {
        "name": name,
        "health": 50,
        "damage": damage
    }

def enemy_attack():
    """Returns a random damage value between 1-10"""
    return random.randint(1, 10)
