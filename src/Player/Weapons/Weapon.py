from math import sqrt, floor
from tkinter import *
from threading import Thread
from time import sleep
from typing import Optional

from Player.Player import *


class Bullet:
    def __init__(self, player, x_destination: int, y_destination: int) -> None:
        self.player = player
        self.canvas: Canvas = self.player.canvas
        self.resource_pack = self.player.resource_pack

        self.start_x = self.player.x
        self.start_y = self.player.y
        self.x = self.player.x
        self.y = self.player.y
        self.end_x = x_destination
        self.end_y = y_destination

        self.bullet_file = PhotoImage(file="resource-packs/" + self.resource_pack + "/weapons/bullet.png")
        self.bullet = self.canvas.create_image(self.x, self.y, anchor=N, image=self.bullet_file)

    def move(self) -> None:
        # just fucking ton of math
        x1 = self.end_x
        y1 = self.end_y
        x2 = self.player.x
        y2 = self.player.y
        c2 = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
        c1 = sqrt((y1 ** 2) + ((x1 * (y2 / y1)) ** 2))
        c = c1 + c2

        ratio = c / y2
        x_ratio = self.start_y / c
        y_ratio = self.start_x / c

        # # index must be going from self.player.y to 0 or other side
        # # we will calculate everything with y
        # c_length = index * ratio
        # new_x = (self.start_y / c) * (index * ratio)
        # new_y = (self.start_x / b) * (index * ratio)

        index = self.y
        print("Starting while loop in move function")
        print("self.x = " + str(self.x) + ", self.y = " + str(self.y))
        while (0 < self.x < 1920) and (0 < self.y < 1080):
            print("Next loop with " + str(self.x) + " as x and " + str(self.y) + " as y")
            new_x = x_ratio * (index * ratio)
            new_y = y_ratio * (index * ratio)

            Thread(target=self.move_image, args=[new_x, new_y, (self.start_y - new_y) / 100]).start()

            self.y = floor(new_y)
            self.x = floor(new_x)
            index -= 1

        print("Ending while loop in move function")
        Thread(target=self.delete_bullet, args=[self.start_y / 100]).start()

    def move_image(self, x: int, y: int, timeout: float) -> None:
        sleep(timeout)
        print("Moving on " + str(x) + ":" + str(y))
        self.canvas.coords(self.bullet, x, y)

    def delete_bullet(self, timeout: int):
        sleep(timeout)
        print("Deleting bullet")
        self.canvas.delete(self.bullet)


class Weapon:
    def __init__(self, player, weapon_name: str, weapon_damage: int = 10, weapon_fire_rate: int = 2) -> None:
        self.player = player
        self.canvas = self.player.canvas

        self.weapon_name = weapon_name
        self.weapon_damage = weapon_damage
        self.weapon_fire_rate = weapon_fire_rate

    def shoot_bullet(self) -> None:
        print("Shooting bullet...")
        bullet = Bullet(self.player, 500, 50)
        Thread(target=bullet.move()).start()
        print("Bullet move ended")


if __name__ == '__main__':
    pass
