"""
weapon file
"""

from math import floor
from tkinter import *
from threading import Thread
from time import sleep
from typing import Optional

from src.Player.Player import *

UP_ = 0
RIGHT_ = 1
DOWN_ = 2
LEFT_ = 3
RIGHT_UP_ = 4
RIGHT_DOWN_ = 5
LEFT_DOWN_ = 6
LEFT_UP_ = 7


class Bullet:
    """
    bullet controller
    """

    def __init__(self, player, weapon, x_destination: int, y_destination: int) -> None:
        self.player = player
        self.weapon = weapon
        self.canvas = self.player.canvas
        self.resource_pack = self.player.resource_pack
        self.destroy_bullet_protocol = False

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

    def __find_destination(self) -> None:
        """
        calculates destination
        """

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

    def __damage_enemy(self, x: int, y: int, timeout: float) -> None:
        """
        damages enemy if in range
        :param x:
        :param y:
        :param timeout:
        :return: Nonetype
        """

        sleep(timeout)

        if self.destroy_bullet_protocol:
            return None

        for enemy in self.player.enemies:
            if enemy.x - 25 < x < enemy.x + 25 and enemy.y - 25 < y < enemy.y + 25 and not enemy.health <= 0:
                Thread(target=self.__delete_bullet, args=[0]).start()

                enemy.take_damage(self.weapon.damage)

    def shoot(self) -> None:
        """
        shoots bullet
        :return: Nonetype
        """

        if self.destination_x == self.start_x and self.destination_y == self.start_y:
            return None

        self.__find_destination()

        to_sleep = 0.005
        while 0 < self.y < 1030 and 30 < self.x < 1890:
            if self.destroy_bullet_protocol:
                return None

            self.y += self.move_by_y
            self.x += self.move_by_x
            Thread(target=self.__move_image, args=[self.x, self.y, to_sleep]).start()

            to_sleep += 0.005

        Thread(target=self.__delete_bullet, args=[to_sleep]).start()

    def __move_image(self, x: int, y: int, timeout: float) -> None:
        """
        moves bullet image
        :param x:
        :param y:
        :param timeout:
        :return: Nonetype
        """

        Thread(target=self.__damage_enemy, args=[x, y, timeout]).start()

        sleep(timeout)

        if self.destroy_bullet_protocol:
            return None

        self.canvas.coords(self.bullet, x, y)

    def __delete_bullet(self, timeout: float) -> None:
        """
        deletes bullet image
        :param timeout:
        :return: Nonetype
        """

        sleep(timeout)

        if self.destroy_bullet_protocol:
            return None

        self.destroy_bullet_protocol = True
        self.canvas.delete(self.bullet)


class Weapon:
    """
    weapon controller
    """

    def __init__(self, player, weapon_damage: int = 10, weapon_fire_rate: int = 2) -> None:
        self.player = player
        self.canvas = self.player.canvas

        self.damage = weapon_damage
        self.fire_rate = weapon_fire_rate
        self.is_shooting_bullet = False

    def shoot_bullet(self, x: int = -404, y: int = -404) -> None:
        """
        shoots bullet
        :param x:
        :param y:
        :return:
        """

        if self.is_shooting_bullet:
            return None

        if x == -404 or y == -404:
            return None

        bullet = Bullet(self.player, self, x, y)
        Thread(target=bullet.shoot).start()

        self.is_shooting_bullet = True
        Thread(target=self.__after_shoot_bullet).start()

    def __after_shoot_bullet(self) -> None:
        """
        after bullet shoot
        """

        sleep(1 / self.fire_rate)
        self.is_shooting_bullet = False


if __name__ == '__main__':
    pass
