from backend import mazegame
from creator import edit_maze
print("<-- WELCOME TO generic maze game!!! -->\n")
choice = input("Would you like to play or enter the maze creator?: ")
if (choice == 'play'):
    mazegame.__init__(mazegame)
elif (choice == 'creator'):
    edit_maze()