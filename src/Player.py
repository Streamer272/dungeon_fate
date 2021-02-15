from threading import Thread
from tkinter import *

from Directions import *


class Player:
    def __init__(self, canvas: Canvas, start_health: int = 100, x: int = 1920 / 2, y: int = 1080 / 2) -> None:
        self.health = start_health
        self.x = x
        self.y = y

        self.canvas = canvas
        self.sprite_file = PhotoImage(file="img/player.png")
        self.sprite = self.canvas.create_image(self.x, self.y, anchor=NW, image=self.sprite_file)

        listener = PlayerListener(self, self.canvas)
        Thread(target=listener.join).start()

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

        self.canvas.move(self.sprite, x, y)


class PlayerListener:
    def __init__(self, player: Player, canvas: Canvas, movement: int = 10):
        self.player = player
        self.canvas = canvas
        self.movement = movement

    def on_press(self, event: any) -> None:
        key = event.char

        if key == "w":
            print("Moving UP")
            self.player.move(UP, self.movement)
        elif key == "d":
            print("Moving RIGHT")
            self.player.move(RIGHT, self.movement)
        elif key == "s":
            print("Moving DOWN")
            self.player.move(DOWN, self.movement)
        elif key == "a":
            print("Moving LEFT")
            self.player.move(LEFT, self.movement)

    def join(self):
        self.canvas.bind_all("<Key>", self.on_press)


if __name__ == '__main__':
    pass
