from tkinter import *
from threading import Thread
from pynput.keyboard import Key, Listener
import time
import random


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


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


class Gui:
    player: Player
    canvas: Canvas
    win: Tk

    def create(self) -> None:
        self.win = Tk()
        self.win.title("2D Game")
        self.win.attributes('-fullscreen', True)

        self.canvas = Canvas(self.win, height=1080, width=1920, bg="white")
        self.canvas.pack()

        self.player = Player(self.canvas, 100)

        self.win.mainloop()

    def do(self) -> None:
        self.player.move(self.canvas, DOWN, 100)


if __name__ == "__main__":
    gui = Gui()
    Thread(target=gui.create).start()
    time.sleep(2)
    gui.do()
