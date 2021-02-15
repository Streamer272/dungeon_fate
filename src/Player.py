from threading import Thread
from tkinter import *
from time import sleep

from Directions import *


class Player:
    def __init__(self, canvas: Canvas, start_health: int = 100, x: int = 1920 / 2, y: int = 1080 / 2) -> None:
        self.health = start_health
        self.x = x
        self.y = y
        self.direction = UP

        self.canvas = canvas
        self.sprite_file = PhotoImage(file="img/player.png")
        self.sprite = self.canvas.create_image(self.x, self.y, anchor=N, image=self.sprite_file)
        self.health_label = canvas.create_text(1840, 20, font="Normal 20 normal normal", text="Health: " + str(self.health))

        listener = PlayerListener(self, self.canvas)
        Thread(target=listener.join).start()

        self.knifing = False
        self.knife_damage = 25
        self.enemies = []

    def move(self, direction: int, steps: int) -> None:
        x = 0
        y = 0

        if direction == UP:
            if self.y - steps <= 0:
                return None

            y -= steps
            self.y -= steps
        elif direction == RIGHT:
            if self.x + steps >= 1900:
                return None

            x += steps
            self.x += steps
        elif direction == DOWN:
            if self.y + steps >= 1030:
                return None

            y += steps
            self.y += steps
        elif direction == LEFT:
            if self.x - steps <= 20:
                return None

            x -= steps
            self.x -= steps

        self.direction = direction
        self.canvas.move(self.sprite, x, y)

    def knife(self) -> None:
        if self.knifing:
            return None

        self.knifing = True
        x = self.x
        y = self.y
        rotation = 0

        if self.direction == UP:
            y -= 50
            rotation = 90
        elif self.direction == RIGHT:
            x += 50
            rotation = 270
        elif self.direction == DOWN:
            y += 50
            rotation = 180
        elif self.direction == LEFT:
            x -= 50
            rotation = 0

        knife_file = PhotoImage(file="img/knife/knife" + str(rotation) + ".png")
        self.canvas.image = knife_file
        knife = self.canvas.create_image(x, y, anchor=N, image=knife_file)
        Thread(target=self.delete_knife, args=(knife, 0.25)).start()

    def delete_knife(self, knife_number, timeout):
        sleep(timeout)
        self.canvas.delete(knife_number)
        self.knifing = False

    def take_damage(self, damage):
        self.health -= damage
        self.canvas.itemconfig(self.health_label, text="Health: " + str(self.health))


class PlayerListener:
    def __init__(self, player: Player, canvas: Canvas, movement: int = 10):
        self.player = player
        self.canvas = canvas
        self.movement = movement

    def on_press(self, event: any) -> None:
        key = str(event.char).lower()

        if key == "w":
            self.player.move(UP, self.movement)
        elif key == "d":
            self.player.move(RIGHT, self.movement)
        elif key == "s":
            self.player.move(DOWN, self.movement)
        elif key == "a":
            self.player.move(LEFT, self.movement)
        elif key == "e":
            self.player.knife()

    def join(self):
        self.canvas.bind_all("w", self.on_press)
        self.canvas.bind_all("d", self.on_press)
        self.canvas.bind_all("s", self.on_press)
        self.canvas.bind_all("a", self.on_press)
        self.canvas.bind_all("e", self.on_press)


if __name__ == '__main__':
    pass
