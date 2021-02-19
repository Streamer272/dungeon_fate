from math import floor
from tkinter import *
from threading import Thread
from time import sleep
from typing import Optional

from Player.Player import *

UP_ = 0
RIGHT_ = 1
DOWN_ = 2
LEFT_ = 3
RIGHT_UP_ = 4
RIGHT_DOWN_ = 5
LEFT_DOWN_ = 6
LEFT_UP_ = 7


class Bullet:
    def __init__(self, player, x_destination: int, y_destination: int) -> None:
        self.player = player
        self.canvas: Canvas = self.player.canvas
        self.resource_pack = self.player.resource_pack

        self.start_x = self.player.x
        self.start_y = self.player.y
        self.x = self.player.x
        self.y = self.player.y + 25
        self.destination_x = x_destination
        self.destination_y = y_destination
        self.move_by_x = 0
        self.move_by_y = 0

        self.bullet_file = PhotoImage(file="resource-packs/" + self.resource_pack + "/weapons/bullet.png")
        self.bullet = self.canvas.create_image(self.x, self.y, anchor=N, image=self.bullet_file)

    def find_destination(self) -> None:
        if self.destination_x - 100 < self.start_x < self.destination_x + 100 and self.destination_y < self.start_y:
            self.move_by_y = -2
        elif self.destination_x - 100 < self.start_x < self.destination_x + 100 and self.destination_y > self.start_y:
            self.move_by_y = 2
        elif self.destination_y - 100 < self.start_y < self.destination_y + 100 and self.destination_x < self.start_x:
            self.move_by_x = -2
        elif self.destination_y - 100 < self.start_y < self.destination_y + 100 and self.destination_x > self.start_x:
            self.move_by_x = 2
        elif self.destination_y < self.start_y and self.destination_x < self.start_x:
            self.move_by_x = -2
            self.move_by_y = -2
        elif self.destination_y < self.start_y and self.destination_x > self.start_x:
            self.move_by_x = 2
            self.move_by_y = -2
        elif self.destination_y > self.start_y and self.destination_x < self.start_x:
            self.move_by_x = -2
            self.move_by_y = 2
        elif self.destination_y > self.start_y and self.destination_x > self.start_x:
            self.move_by_x = 2
            self.move_by_y = 2

    def move(self) -> None:
        if self.destination_x == self.start_x and self.destination_y == self.start_y:
            return None

        self.find_destination()

        to_sleep = 0.005
        while 0 < self.y < 1030 and 30 < self.x < 1890:
            self.y += self.move_by_y
            self.x += self.move_by_x
            Thread(target=self.move_image, args=[self.x, self.y, to_sleep]).start()
            to_sleep += 0.005

        Thread(target=self.delete_bullet, args=[to_sleep]).start()

    def move_image(self, x: int, y: int, timeout: float) -> None:
        sleep(timeout)
        self.canvas.coords(self.bullet, x, y)

    def delete_bullet(self, timeout: int):
        sleep(timeout)
        self.canvas.delete(self.bullet)


class Weapon:
    def __init__(self, player, weapon_damage: int = 10, weapon_fire_rate: int = 2) -> None:
        self.player = player
        self.canvas = self.player.canvas

        self.damage = weapon_damage
        self.fire_rate = weapon_fire_rate
        self.is_shooting_bullet = False

    def shoot_bullet(self, x, y) -> None:
        if self.is_shooting_bullet:
            return None

        bullet = Bullet(self.player, x, y)
        Thread(target=bullet.move).start()

        self.is_shooting_bullet = True
        Thread(target=self.after_shoot_bullet).start()

    def after_shoot_bullet(self) -> None:
        sleep(1 / self.fire_rate)
        self.is_shooting_bullet = False


if __name__ == '__main__':
    pass
