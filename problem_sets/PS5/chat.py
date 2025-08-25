"""
Chat with Claude about Animals - PS5 Final Part
Integrates Claude API with the zoo management system
"""

import sys
import os

# Add the project root to Python path to access Claude practice modules
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
claude_practice_path = os.path.join(project_root, 'Claude practice')
sys.path.insert(0, claude_practice_path)

# Import our classes
from zoo import Animal, Bird, Caretaker
from ai_tools.ai_assistant import AIAssistant

def main():
    """Main function to demonstrate Claude integration with zoo animals"""
    print("🦁 Welcome to the AI-Powered Zoo Management System!")
    print("=" * 60)
    
    # Initialize Claude AI Assistant
    try:
        # Use Claude 3.5 Sonnet for best results
        assistant = AIAssistant(model="claude-3-5-sonnet-20241022")
        print("✓ Claude AI Assistant initialized successfully!")
    except Exception as e:
        print(f"✗ Error initializing Claude: {e}")
        return
    
    print("\nWhat would you like to do?")
    print("1. Get information about an animal")
    print("2. Create a new animal with Claude's help")
    print("3. Both - Get info and create animal")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        # Get information about an animal
        animal_name = input("\n🐾 Enter an animal name to learn about: ").strip()
        
        if animal_name:
            print(f"\n🤔 Asking Claude about {animal_name}...")
            
            # Create a system prompt for animal information
            system_prompt = """You are a knowledgeable zoologist. Provide interesting, 
            educational information about animals. Keep responses concise but informative, 
            focusing on interesting facts, habitat, behavior, and characteristics."""
            
            # Ask Claude about the animal
            question = f"Tell me interesting facts about {animal_name}. Include information about their habitat, behavior, and unique characteristics."
            
            try:
                response = assistant.chat(
                    message=question,
                    system_prompt=system_prompt,
                    max_tokens=500,
                    temperature=0.7
                )
                
                print(f"\n🧠 Claude's response about {animal_name}:")
                print("-" * 50)
                print(response)
                print("-" * 50)
                
            except Exception as e:
                print(f"✗ Error getting information from Claude: {e}")
                return
    
    if choice in ['2', '3']:
        # Create a new animal with Claude's help
        print("\n🏗️  Let's create a new animal object!")
        
        animal_name = input("Enter the animal's name: ").strip()
        if not animal_name:
            animal_name = "Unknown Animal"
            
        # Ask Claude to provide structured information for creating an animal
        structure_prompt = """You are helping to create animal objects for a zoo management system. 
        Provide realistic information in a structured format."""
        
        question = f"""For an animal named {animal_name}, provide:
        1. Species (be specific, e.g., 'African Lion' not just 'Lion')
        2. Typical age (just a number, realistic for zoo animals)
        3. One interesting fact about this species
        
        Format your response exactly like this:
        Species: [species name]
        Age: [number]
        Fact: [interesting fact]"""
        
        try:
            structured_response = assistant.chat(
                message=question,
                system_prompt=structure_prompt,
                max_tokens=200,
                temperature=0.5
            )
            
            print(f"\n🤖 Claude's structured response:")
            print(structured_response)
            
            # Parse Claude's response to create an Animal object
            lines = structured_response.strip().split('\n')
            species = "Unknown Species"
            age = 5  # default
            fact = "No additional information available."
            
            for line in lines:
                if line.startswith("Species:"):
                    species = line.split(":", 1)[1].strip()
                elif line.startswith("Age:"):
                    try:
                        age = int(line.split(":", 1)[1].strip())
                    except ValueError:
                        age = 5
                elif line.startswith("Fact:"):
                    fact = line.split(":", 1)[1].strip()
            
            # Create the animal object
            new_animal = Animal(animal_name, species, age)
            new_animal.add_ai_info(fact)
            
            print(f"\n🎉 Created new animal:")
            print(f"   {new_animal.describe()}")
            print(f"   AI Fact: {new_animal.ai_info}")
            
        except Exception as e:
            print(f"✗ Error creating animal with Claude's help: {e}")
            return
    
    print(f"\n✅ Demo completed successfully!")
    print("You can now use Claude AI throughout your entire ai-dev-learning project!")

if __name__ == "__main__":
    main()
