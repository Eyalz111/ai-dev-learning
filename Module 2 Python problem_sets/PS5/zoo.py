"""
Zoo Management System - PS5
Contains Animal, Bird, and Caretaker classes for managing zoo animals
"""


class Animal:
    """Base Animal class with basic attributes and methods"""
    
    def __init__(self, name, species, age):
        """
        Initialize an Animal with basic attributes
        
        Args:
            name (str): The animal's name
            species (str): The animal's species
            age (int): The animal's age
        """
        self.name = name
        self.species = species
        self.age = age
    
    def describe(self):
        """Return a formatted string with the animal's details"""
        return f"{self.name} is a {self.age}-year-old {self.species}."
    
    def make_sound(self):
        """Generic method for making sound - to be overridden by subclasses"""
        return "The animal makes a sound"
    
    def add_ai_info(self, ai_info):
        """Add AI-generated information about this animal"""
        self.ai_info = ai_info
        return f"Added AI information for {self.name}: {ai_info[:100]}..."


class Caretaker:
    """Caretaker class representing a person who takes care of animals"""
    
    def __init__(self, name, experience_years):
        """
        Initialize a Caretaker
        
        Args:
            name (str): The caretaker's name
            experience_years (int): Number of years of experience
        """
        self.name = name
        self.experience_years = experience_years
    
    def describe(self):
        """Return a formatted string with the caretaker's details"""
        return f"{self.name} has {self.experience_years} years of experience caring for animals."


class Bird(Animal):
    """Bird class inheriting from Animal with additional wing-related features and caretaker"""
    
    def __init__(self, name, species, age, wing_span, caretaker):
        """
        Initialize a Bird with all Animal attributes plus wing_span and caretaker
        
        Args:
            name (str): The bird's name
            species (str): The bird's species
            age (int): The bird's age
            wing_span (int): Wing span from tip to tip in centimeters
            caretaker (Caretaker): The caretaker object responsible for this bird
        """
        super().__init__(name, species, age)  # Call parent constructor
        self.wing_span = wing_span
        self.caretaker = caretaker  # Composition: Bird HAS-A Caretaker
    
    def describe_wings(self):
        """Return a formatted string describing the bird's wings"""
        return f"{self.name} has a wingspan of {self.wing_span} cm."
    
    def make_sound(self):
        """Override the generic sound method for birds"""
        return "Tweet tweet!"
    
    def describe_with_caretaker(self):
        """Return a description including both bird and caretaker information"""
        bird_info = self.describe()
        caretaker_info = self.caretaker.describe()
        return f"{bird_info}\n{caretaker_info}"
