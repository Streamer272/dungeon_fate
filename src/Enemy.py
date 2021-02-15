from threading import Thread
from tkinter import *
from time import sleep
from random import randint

from Player import *


class Enemy:
    def __init__(self, canvas: Canvas, player: Player, start_health: int = 50) -> None:
        self.player = player
        self.health = start_health
        self.x = randint(100, 1820)
        self.y = randint(100, 980)

        self.canvas = canvas
        self.enemy_file = PhotoImage(file="img/enemy.png")
        self.enemy = self.canvas.create_image(self.x, self.y, anchor=N, image=self.enemy_file)

    def auto_move(self):
        while self.health != 0:
            sleep(0.5)

            x = 0
            y = 0

            if self.player.x < self.x:
                x -= 50

            if self.player.y < self.y:
                y -= 50

            if self.player.y > self.y:
                y += 50

            if self.player.x > self.x:
                x += 50

            self.x += x
            self.y += y

            self.canvas.move(self.enemy, x, y)


if __name__ == '__main__':
    pass
