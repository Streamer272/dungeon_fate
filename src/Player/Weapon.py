from math import sqrt, floor
from tkinter import *
from threading import Thread
from time import sleep

from Player.Player import *


class Weapon:
    def __init__(self, player, weapon_name: str, weapon_damage: int = 10, weapon_fire_rate: int = 2):
        self.player = player
        self.canvas = self.player.canvas

        self.weapon_name = weapon_name
        self.weapon_damage = weapon_damage
        self.weapon_fire_rate = weapon_fire_rate

    def get_bullet_track(self, x1, y1):
        print("Getting bullet track...")
        y2 = self.player.y
        x3 = x1 * (y2 / y1)

        index = 0
        pixel_coordinates = []
        ratio = y2 / x3
        while index != x3:
            pixel_coordinates.append([index, floor(index * ratio)])
            index += 1

        return pixel_coordinates

    def shoot_bullet(self, trajectories):
        print("Shooting bullet...")
        bullet_image = PhotoImage(file="img/bullet.png")
        self.canvas.image = bullet_image
        bullet = self.canvas.create_image(0, 0, anchor=N, image=bullet_image)
        Thread(target=self.move_bullet, args=(trajectories, bullet)).start()

    def move_bullet(self, trajectories, bullet):
        print("Moving bullet")
        for i in range(len(trajectories)):
            trajectory = trajectories[-i-1]
            print("Moving on " + str(trajectory))
            self.canvas.coords(bullet, trajectory[0], trajectory[1])
            sleep(0.01)


if __name__ == '__main__':
    pass
