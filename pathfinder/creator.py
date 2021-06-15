'''
This program's purpose is to create an a blank grid which can be turned into a maze via a interactible GUI
'''
import pygame as pg
import pandas as pd
import os
def open_maze(file_name):
    path = os.getcwd() + '/maps/' + file_name + '.csv'
    df = pd.read_csv(path)
    grid = []
    for row in df.itertuples(index=False, name=None):
        grid.append(list(row))
    pg.display.set_caption("Maze Editor: " + file_name.capitalize())
    return grid

def refresh(new_grid, width_iter, height_iter, screen, screen_width, screen_height):
    new_y = 0
    for row in new_grid:
        new_x = 0
        for box in row:
            if (box == 0):
                color = 'black'
            elif (box == 1):
                color = (42, 42, 42)
            elif (box == 2):
                color = (13, 96, 37)
            elif (box == 3):
                color = 'red'
            pg.draw.rect(screen, color, (new_x, new_y, new_x + width_iter, new_y + height_iter))
            new_x += width_iter
        new_y += height_iter
    # Drawing the grid lines
    i = 1
    for row in new_grid:
        pg.draw.line(screen, 'white', (0, height_iter * i), (screen_height, height_iter * i))
        pg.draw.line(screen, 'white', (width_iter * i, 0), (width_iter * i, screen_width))
        i += 1
    pg.display.update()

def show_maze(grid):
    pg.init()
    size = width, height = 750, 750
    screen = pg.display.set_mode(size)
    screen.fill('black')
    width_iter, height_iter = (size[0] / len(grid[0]), size[1] / len(grid))
    # Filling in the boxes
    refresh(grid, width_iter, height_iter, screen, size[0], size[1])
    return width_iter, height_iter, size[0], size[1], screen

def get_cursor_coordinates(grid, cursorx, cursory, screenx, screeny):
    grid_height, grid_width = (len(grid), len(grid[0]))
    width_iter, height_iter = (screenx / len(grid[0]), screeny / len(grid))
    column_list = []
    for column in range(grid_width + 1):
        column_list.append(width_iter * column)
    row_list = []
    for row in range(grid_height + 1):
        row_list.append(height_iter * row)
    for column in column_list:
        if (cursorx < column):
            x_target = column_list.index(column) - 1
            break
    for row in row_list:
        if (cursory < row):
            y_target = row_list.index(row) - 1
            break
    # print("Coordinates: ({}, {})".format(x_target, y_target))
    return x_target, y_target

def swap_out(grid, click_type, coordinates):
    target_row = grid[coordinates[1]]
    if (click_type == "l_click"):
        target_row.pop(coordinates[0])
        target_row.insert(coordinates[0], 1)
    elif (click_type == "r_click"):
        target_row.pop(coordinates[0])
        target_row.insert(coordinates[0], 0)
    elif (click_type == "z_click"):
        target_row.pop(coordinates[0])
        target_row.insert(coordinates[0], 2)
    elif (click_type == "x_click"):
        target_row.pop(coordinates[0])
        target_row.insert(coordinates[0], 3)
    return grid

def save_maze(grid_to_save):
    file_name = input("To save the grid either enter the same filename to save it or enter a new one to create a new file: ")
    nf = pd.DataFrame(grid_to_save)
    path = os.getcwd() + '/maps/' + file_name + '.csv'
    nf.to_csv(path, index=False)


def create_maze():
    '''
    Ask for the desired width and height preferrably having them be equal.
    create the basic grid and everytime they change something re-graph the lines.
    write maze to a new csv of their filename choice
    '''
    height = int(input("What would you like the height of your maze to be?: "))
    width = int(input("What would you like the width of your maze to be?: "))
    grid = []
    for i in range(height):
        grid.append([])
        for j in range(width):
            row_target = grid[i]
            row_target.append(0)
    return grid

def expand_maze(grid, screenx, screeny):
    print("KEY: LEFT, TOP, RIGHT, BOTTOM")
    print("KEY: EXPAND >= 1, CONTRACT <= -1, NOTHING = 0")
    sides_to_expand = input("What sides would you like to expand or contract? (Please provide with seperated commas): ")
    sides_to_expand = tuple(int(x) for x in sides_to_expand.split(","))
    i = 1
    for side in sides_to_expand:
        i_side = int(str(side).lstrip('-+'))
        for action in range(i_side):
            grid_width = len(grid[0])
            grid_height = len(grid)
            if (i == 1):
                position = 0
            if (i == 2):
                position = 0
            elif (i == 3):
                position = grid_width
            elif (i == 4):
                position = grid_height
            if (side >= 1):
                if (i == 1 or i == 3):
                    for row in grid:
                        row.insert(position, 0)
                else:
                    replacement = []
                    for w in range(grid_width):
                        replacement.append(0)
                    grid.insert(position, replacement)
            elif (side <= -1):
                if (i == 1):
                    for row in grid:
                        row.pop(position)
                elif (i == 3):
                    for row in grid:
                        row.pop(position - 1)
                elif (i == 4):
                    grid.pop(position - 1)
                else:
                    grid.pop(position)
        i += 1
    width_iter, height_iter = (screenx / len(grid[0]), screeny / len(grid))
    return grid, width_iter, height_iter

def edit_maze():
    choice = input("Would you like to create a new maze or edit an existing one? (create/edit): ")
    if (choice == 'create'):
        print("Starting up the maze creator...")
        grid = create_maze()
    elif (choice == 'edit'):
        maze_name = input("What is the filename of the maze you would like to edit? (excluding the endfix): ")
        grid = open_maze(maze_name)
    else:
        print("Not a valid choice.")
        edit_maze()
        quit()
    print("Starting up the maze editor.")
    width_iter, height_iter, screen_width, screen_height, screen = show_maze(grid)
    pg.display.update()
    new_grid = grid
    message = "Press 'E' to edit borders, 'Lmb' to place a wall, 'Rmb' to erase,\n'S' to save, 'Z' to place the starting point, and 'X' to place an exit. "
    while True: #While loop that constantly checks for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            # Left Click
            elif pg.mouse.get_pressed() == (1, 0, 0):
                mouse_pos = pg.mouse.get_pos()
                grid_target = get_cursor_coordinates(grid, mouse_pos[0], mouse_pos[1], screen_width, screen_height)
                new_grid = swap_out(grid, "l_click", grid_target)
                refresh(new_grid, width_iter, height_iter, screen, screen_width, screen_height)
            # Right Click
            elif pg.mouse.get_pressed() == (0, 0, 1):
                mouse_pos = pg.mouse.get_pos()
                grid_target = get_cursor_coordinates(grid, mouse_pos[0], mouse_pos[1], screen_width, screen_height)
                new_grid = swap_out(grid, "r_click", grid_target)
                refresh(new_grid, width_iter, height_iter, screen, screen_width, screen_height)
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key == pg.K_z:
                    mouse_pos = pg.mouse.get_pos()
                    grid_target = get_cursor_coordinates(grid, mouse_pos[0], mouse_pos[1], screen_width, screen_height)
                    new_grid = swap_out(grid, "z_click", grid_target)
                    refresh(new_grid, width_iter, height_iter, screen, screen_width, screen_height)
                elif key == pg.K_x:
                    mouse_pos = pg.mouse.get_pos()
                    grid_target = get_cursor_coordinates(grid, mouse_pos[0], mouse_pos[1], screen_width, screen_height)
                    new_grid = swap_out(grid, "x_click", grid_target)
                    refresh(new_grid, width_iter, height_iter, screen, screen_width, screen_height)
                elif key == pg.K_s:
                    save_maze(new_grid)
                    pg.quit()
                    quit()
                elif key == pg.K_e:
                    new_grid, width_iter, height_iter = expand_maze(new_grid, screen_width, screen_height)
                    refresh(new_grid, width_iter, height_iter, screen, screen_width, screen_height)
                elif key == pg.K_h:
                    print(message)