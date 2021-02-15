from tkinter import *
from Directions import *


class Player:
    def __init__(self, canvas: Canvas, start_health: int = 100, x: int = 1920 / 2, y: int = 1080 / 2) -> None:
        self.health = start_health
        self.x = x
        self.y = y

        self.sprite_file = PhotoImage(file="src/img/player.png")
        self.sprite = canvas.create_image(self.x, self.y, anchor=NW, image=self.sprite_file)

    def move(self, canvas: Canvas, direction: int, steps: int) -> None:
        x = 0
        y = 0

        if direction == UP:
            y -= steps
            self.y -= steps
        elif direction == RIGHT:
            x += steps
            self.x += steps
        elif direction == DOWN:
            y += steps
            self.y += steps
        elif direction == LEFT:
            x -= steps
            self.x -= steps

        canvas.move(self.sprite, x, y)


if __name__ == '__main__':
    pass
