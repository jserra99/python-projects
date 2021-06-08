import creator
from backend import *

print("<-- WELCOME TO generic maze game!!! -->\n")
choice = input("Would you like to play or edit/create a maze? (p/e): ")
if (choice == 'p'):
    # Play the damn game
    # Ask about which map they want to use
    # Somehow displau that map
    pass
elif (choice == 'e'):
    creator.edit_maze()
