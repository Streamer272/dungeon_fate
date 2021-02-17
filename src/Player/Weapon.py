from math import sqrt, floor
from tkinter import *
from threading import Thread
from time import sleep
from typing import Optional

from Player.Player import *


class Bullet:
    def __init__(self, player, x_destination: int, y_destination: int) -> None:
        self.player = player
        self.canvas = self.player.canvas

        self.start_x = self.player.x
        self.start_y = self.player.y
        self.x = self.player.x
        self.y = self.player.y
        self.end_x = x_destination
        self.end_y = y_destination

        self.bullet_file = PhotoImage(file="img/bullet.png")
        self.bullet = self.canvas.create_image(self.x, self.y, anchor=N, image=self.bullet_file)

    def move(self):
        x1 = self.end_x
        y1 = self.end_y
        x2 = self.player.x
        y2 = self.player.y
        c2 = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
        c1 = sqrt((y1 ** 2) + ((x1 * (y2 / y1)) ** 2))
        ratio = (c1 + c2) / y2
        while 0 < self.x < 1920 and 0 < self.y < 1080:
            pass


class Weapon:
    def __init__(self, player, weapon_name: str, weapon_damage: int = 10, weapon_fire_rate: int = 2) -> None:
        self.player = player
        self.canvas = self.player.canvas

        self.weapon_name = weapon_name
        self.weapon_damage = weapon_damage
        self.weapon_fire_rate = weapon_fire_rate

    def shoot_bullet(self) -> None:
        print("Shooting bullet...")
        bullet = Bullet(self.player, 200, 900)
        bullet.move()

        print("While loop ended")

        self.canvas.delete(bullet.bullet)


if __name__ == '__main__':
    pass
