#!/usr/bin/env python3
"""
Test script for the save system functionality.
Tests creating, saving, loading, and updating player data.
"""

from save_system import save_game, load_game, update_player_stats
from game_tools.player import create_player

def main():
    print("=== Save System Test ===\n")
    
    # Step 1: Create a new player with all required fields
    print("1. Creating a new player...")
    player = create_player("TestHero")
    # Add inventory to the player (the create_player function doesn't include it)
    player["inventory"] = ["sword", "potion", "map"]
    
    print(f"Initial player data: {player}")
    print()
    
    # Step 2: Save the player data
    print("2. Saving player data...")
    save_game(player, "test_savegame.json")
    print()
    
    # Step 3: Load the player data back
    print("3. Loading player data...")
    loaded_player = load_game("test_savegame.json")
    print(f"Loaded player data: {loaded_player}")
    print()
    
    # Step 4: Update the stats
    print("4. Updating player stats...")
    print("Before update:", loaded_player)
    updated_player = update_player_stats(loaded_player)
    print("After update:", updated_player)
    print()
    
    # Step 5: Save the updated data
    print("5. Saving updated player data...")
    save_game(updated_player, "test_savegame.json")
    print()
    
    # Step 6: Load one more time to verify everything worked
    print("6. Final verification - loading updated data...")
    final_player = load_game("test_savegame.json")
    print(f"Final player data: {final_player}")
    print()
    
    # Verify the changes
    print("=== Verification ===")
    print(f"Original health: 100, Final health: {final_player['health']}")
    print(f"Original score: 0, Final score: {final_player['score']}")
    print(f"Original inventory: ['sword', 'potion', 'map']")
    print(f"Final inventory: {final_player['inventory']}")
    
    if final_player['health'] == 110 and final_player['score'] == 50 and 'shield' in final_player['inventory']:
        print("\n✅ All tests passed! Save system is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the save system functions.")

if __name__ == "__main__":
    main()
