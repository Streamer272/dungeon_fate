from threading import Thread
from tkinter import *
from time import sleep
from random import randint

from Directions import *


class Enemy:
    def __init__(self, canvas: Canvas, start_health: int = 50, x: int = 1920 / 2, y: int = 1080 / 2) -> None:
        self.health = start_health
        self.x = x
        self.y = y
        self.direction = UP

        self.canvas = canvas
        self.enemy_file = PhotoImage(file="img/enemy.png")
        self.sprite = self.canvas.create_image(self.x, self.y, anchor=N, image=self.enemy_file)

    def move(self, direction: int, steps: int) -> None:
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

        self.direction = direction
        self.canvas.move(self.sprite, x, y)


if __name__ == '__main__':
    pass
