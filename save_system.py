import json
import os

def save_game(player_data, filename="savegame.json"):
    """Save player data to a JSON file"""
    with open(filename, "w") as f:
        json.dump(player_data, f, indent=4)  # indent=4 makes it pretty!
    print(f"Game saved to {filename}")

def load_game(filename="savegame.json"):
    """Load player data from JSON file"""
    # Check if save file exists
    if not os.path.exists(filename):
        print("No save file found!")
        return None
    
    with open(filename, "r") as f:
        player_data = json.load(f)
    print("Game loaded!")
    return player_data

def update_player_stats(player_data):
    """
    Update the player stats and return the modified data
    - Add 10 to health 
    - Add 50 to score
    - Add "shield" to inventory if there's an inventory list
    """
    player_data["health"] += 10
    player_data["score"] += 50
    
    if "inventory" in player_data and isinstance(player_data["inventory"], list):
        player_data["inventory"].append("shield")
        
    return player_data