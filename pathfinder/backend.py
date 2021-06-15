import pygame as pg
import pandas as pd
import os

class mazegame():
    ''''''
    def __init__(self):
        self.file_name = input("What is the maze you would like to play?: ")
        self.path = os.getcwd() + '/maps/' + self.file_name + '.csv'
        self.df = pd.read_csv(self.path)
        self.grid = []
        for row in self.df.itertuples(index=False, name=None):
            self.grid.append(list(row))
        pg.init()
        self.size = self.screen_width, self.screen_height = 750, 750
        self.screen = pg.display.set_mode(self.size)
        self.screen.fill('black')
        pg.display.set_caption("Pathfinder")
        self.width_iter, self.height_iter = (self.screen_width / len(self.grid[0]), self.screen_height / len(self.grid))
        self.sprite_width, self.sprite_height = self.width_iter * (3/4), self.height_iter * (3/4)
        self.truths = {
            "canMoveLeft": False,
            "canMoveRight": False,
            "canMoveForward": False,
            "canMoveBackward": False,
            "currentX": 0,
            "currentY": 0,
            "currentOrientation": "Forward",
            "endX": 0,
            "endY": 0,
            "isStarting": True,
            "hasWon": False
        }
        self.refresh(self)
        self.game_start_manual(self)
    
    def refresh(self):
        new_y = 0
        for row in self.grid:
            new_x = 0
            for box in row:
                if (box == 0):
                    color = 'black'
                elif (box == 1):
                    color = (42, 42, 42)
                elif (box == 2):
                    color = (13, 96, 37)
                    self.startX = int(round(new_x / self.width_iter, 1))
                    self.startY = int(round(new_y / self.height_iter, 1))
                elif (box == 3):
                    color = 'red'
                    self.truths.pop("endX")
                    self.truths.pop("endY")
                    self.truths.update({"endX": int(round(new_x / self.width_iter, 1)), "endY": int(round(new_y / self.height_iter, 1))})
                pg.draw.rect(self.screen, color, (new_x, new_y, new_x + self.width_iter, new_y + self.height_iter))
                new_x += self.width_iter
            new_y += self.height_iter
        i = 1
        for row in self.grid:
            pg.draw.line(self.screen, 'white', (0, self.height_iter * i), (self.screen_height, self.height_iter * i))
            pg.draw.line(self.screen, 'white', (self.width_iter * i, 0), (self.width_iter * i, self.screen_width))
            i += 1
        # Add in some code to render in sprite
        sprite_x, sprite_y, orientation = (self.truths.get("currentX"), self.truths.get("currentY"), self.truths.get("currentOrientation"))
        if (self.truths.get("isStarting")):
            sprite_x = self.startX
            sprite_y = self.startY
            self.truths.pop("currentX")
            self.truths.pop("currentY")
            self.truths.update({"currentX": sprite_x, "currentY": sprite_y})
            self.truths.pop("isStarting")
            self.truths.update({"isStarting": False})
        if (sprite_x != 0 and sprite_y != 0):
            pg.draw.rect(
                self.screen,
                'white',
                (
                    (self.width_iter * sprite_x) + (self.width_iter * (1/8)),
                    (self.height_iter * sprite_y) + (self.height_iter * (1/8)),
                    self.sprite_width + 2,
                    self.sprite_height + 2
                )
            )
            
        elif (sprite_x == 0 and sprite_y != 0):
            pg.draw.rect(
                self.screen,
                'white',
                (
                    self.width_iter * (1/8),
                    (self.height_iter * sprite_y) + (self.height_iter * (1/8)),
                    self.sprite_width + 2,
                    self.sprite_height + 2
                )
            )
        elif (sprite_y == 0 and sprite_x != 0):
            pg.draw.rect(
                self.screen,
                'white',
                (
                    (self.width_iter * sprite_x) + (self.width_iter * (1/8)),
                    self.height_iter * (1/8),
                    self.sprite_width + 2,
                    self.sprite_height + 2
                )
            )
        else:
            # They both are zero
            pg.draw.rect(
                self.screen,
                'white',
                (
                    self.width_iter * (1/8),
                    self.height_iter * (1/8),
                    self.sprite_width + 2,
                    self.sprite_height + 2
                )
            )
        pg.display.update()

    def move(self, direction):
        if (direction == 'forward'):
            # Move forward
            y_val = self.truths.get("currentY") - 1
            self.truths.pop("currentY")
            self.truths.update({"currentY": y_val})
        elif (direction == 'backward'):
            # Move backward
            y_val = self.truths.get("currentY") + 1
            self.truths.pop("currentY")
            self.truths.update({"currentY": y_val})
        elif (direction == 'right'):
            # Move right
            x_val = self.truths.get("currentX") + 1
            self.truths.pop("currentX")
            self.truths.update({"currentX": x_val})
        else:
            x_val = self.truths.get("currentX") - 1
            self.truths.pop("currentX")
            self.truths.update({"currentX": x_val})
        self.refresh(self)
        self.update_truths(self)

    def update_truths(self):
        # Check in what direction the sprite can move
        # Update those values in the dictionary and set them to variables
        sprite_x, sprite_y, orientation = (self.truths.get("currentX"), self.truths.get("currentY"), self.truths.get("currentOrientation"))
        # Checking if can move left
        if (self.grid[sprite_y][sprite_x -1] != 1):
            canMoveLeft = True
        else:
            canMoveLeft = False
        if (self.grid[sprite_y][sprite_x + 1] != 1):
            canMoveRight = True
        else:
            canMoveRight = False
        if (self.grid[sprite_y - 1][sprite_x] != 1):
            canMoveForward = True
        else:
            canMoveForward = False
        if (self.grid[sprite_y + 1][sprite_x] != 1):
            canMoveBackward = True
        else:
            canMoveBackward = False
        if (sprite_x == self.truths.get("endX") and sprite_y == self.truths.get("endY")):
            hasWon = True
            print("You have won.")
        else:
            hasWon = False
        self.truths.pop("canMoveLeft")
        self.truths.pop("canMoveRight")
        self.truths.pop("canMoveForward")
        self.truths.pop("canMoveBackward")
        self.truths.pop("hasWon")
        self.truths.update({"canMoveLeft": canMoveLeft, "canMoveRight": canMoveRight, "canMoveForward": canMoveForward, "canMoveBackward": canMoveBackward, "hasWon": hasWon})

    def game_start_manual(self):
        self.update_truths(self)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    key = event.key
                    if key == pg.K_UP:
                        if (self.truths.get("canMoveForward")):
                            self.move(self, 'forward')
                    elif key == pg.K_DOWN:
                        if (self.truths.get("canMoveBackward")):
                            self.move(self, 'backward')
                    elif key == pg.K_RIGHT:
                        if (self.truths.get("canMoveRight")):
                            self.move(self, 'right')
                    elif key == pg.K_LEFT:
                        if (self.truths.get("canMoveLeft")):
                            self.move(self, 'left')