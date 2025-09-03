"""
Main file for PS5 - Zoo Management System
Imports Bird class from zoo module and demonstrates its functionality
"""

from zoo import Bird, Caretaker

# Create a caretaker
caretaker = Caretaker("Dina", 5)

# Create a parrot with the caretaker
parrot = Bird("Polly", "Parrot", 3, 25, caretaker)

# Demonstrate all the functionality
print(parrot.describe())                    # Polly is a 3-year-old Parrot.
print(parrot.describe_wings())              # Polly has a wingspan of 25 cm.
print(parrot.make_sound())                  # Tweet tweet!
print(parrot.caretaker.describe())          # Dina has 5 years of experience caring for animals.
