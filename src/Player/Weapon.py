from math import sqrt, floor
from tkinter import *
from threading import Thread
from time import sleep

from Player.Player import *


LEFT_UP = 0
RIGHT_UP = 1
RIGHT_DOWN = 2
LEFT_DOWN = 3


class Bullet:
    def __init__(self, player, x: int, y: int):
        self.player = player
        self.canvas = self.player.canvas

        self.x_percent = x / 100
        self.y_percent = y / 100
        self.x = x
        self.y = y

        self.bullet_file = PhotoImage(file="img/bullet.png")
        self.bullet = self.canvas.create_image(self.x, self.y, anchor=N, image=self.bullet_file)

    def get_direction_by_coordinates(self):
        if self.player.x > self.x and self.player.y > self.y:
            return RIGHT_DOWN
        elif self.player.x < self.x and self.player.y > self.y:
            return LEFT_DOWN
        elif self.player.x < self.x and self.player.y < self.y:
            return LEFT_UP
        elif self.player.x > self.x and self.player.y < self.y:
            return RIGHT_UP
        else:
            return None

    def move_next(self):
        direction = self.get_direction_by_coordinates()

        if direction == LEFT_UP:
            self.x = self.x - self.x_percent
            self.y = self.y - self.y_percent
        elif direction == RIGHT_UP:
            self.x = self.x + self.x_percent
            self.y = self.y - self.y_percent
        elif direction == RIGHT_DOWN:
            self.x = self.x - self.x_percent
            self.y = self.y + self.y_percent
        elif direction == LEFT_DOWN:
            self.x = self.x + self.x_percent
            self.y = self.y + self.y_percent
        elif direction is None:
            raise TypeError

        self.canvas.coords(self.bullet, self.x, self.y)


class Weapon:
    def __init__(self, player, weapon_name: str, weapon_damage: int = 10, weapon_fire_rate: int = 2):
        self.player = player
        self.canvas = self.player.canvas

        self.weapon_name = weapon_name
        self.weapon_damage = weapon_damage
        self.weapon_fire_rate = weapon_fire_rate

    def shoot_bullet(self):
        print("Shooting bullet...")
        bullet = Bullet(self.player, self.player.x, self.player.y)

        while bullet.x > 0 and bullet.y > 0 and bullet.x < 1920 and bullet.y < 1080:
            bullet.move_next()

    def move_bullet(self):
        print("Moving bullet")


if __name__ == '__main__':
    pass
