"""
enemy file
"""

from random import randint, choice
from math import floor
from tkinter import *
from threading import Thread
from time import sleep

from src.Player.Player import *


class Enemy:
    """
    enemy controller
    """

    def __init__(self, player: Player, health: int = 50, damage: int = 10,
                 attack_speed: float = 0.5) -> None:
        if player.health <= 0:
            return

        self.player = player
        self.health = health
        self.game_running = True
        self.despawn_timer = 10
        self.direction = 0

        self.damage = damage
        self.charging_attack = False
        self.attack_speed = attack_speed

        self.x, self.y = self.__generate_spawn_position()

        self.canvas = player.canvas
        self.resource_pack = self.player.resource_pack
        self.dont_change_image_protocol = False
        self.current_image_file = "resource-packs/" + self.resource_pack + "/enemy/movement/enemy" + str(self.direction) + ".png"
        self.enemy_file = PhotoImage(file=self.current_image_file)
        self.enemy = self.canvas.create_image(self.x, self.y, anchor=N, image=self.enemy_file)

    def __del__(self):
        self.__delete()

    def __generate_spawn_position(self) -> tuple:
        """
        generates random position for enemy
        :return: tuple
        """

        x_possible = [[self.player.x - 500, self.player.x - 250], [self.player.x + 250, self.player.x + 500]]
        y_possible = [[self.player.y - 500, self.player.y - 250], [self.player.y + 250, self.player.y + 500]]
        x_choice = choice(x_possible)
        y_choice = choice(y_possible)
        x = randint(floor(x_choice[0]), floor(x_choice[1]))
        y = randint(floor(y_choice[0]), floor(y_choice[1]))

        if x < 0 or y < 0 or x > 1920 or y > 1080:
            x, y = self.__generate_spawn_position()

        if x % 5 != 0 or y % 5 != 0:
            x, y = self.__generate_spawn_position()

        return x, y

    def __attack_player(self) -> None:
        """
        attacks player if in range
        :return: Nonetype
        """

        if self.player.invisible:
            return None

        if self.player.x - 50 < self.x < self.player.x + 50 and self.player.y - 50 < self.y < self.player.y + 50 and not self.charging_attack:
            self.player.take_damage(self.damage)
            self.charging_attack = True
            Thread(target=self.__charge_attack).start()

    def __charge_attack(self) -> None:
        """
        recharges attack after attacking player
        """

        sleep(1 / self.attack_speed)
        self.charging_attack = False

    def take_damage(self, damage: int) -> None:
        """
        takes damage from any source
        :param damage:
        :return: Nonetype
        """

        if self.health <= 0:
            return None

        self.health -= damage

        if self.health <= 0:
            self.__start_die_animation()
            return None

        if not self.current_image_file == "resource-packs/" + self.resource_pack + "/enemy/damaged/enemy-damaged" + str(self.direction) + ".png" and not self.dont_change_image_protocol:
            self.dont_change_image_protocol = True
            self.current_image_file = "resource-packs/" + self.resource_pack + "/enemy/damaged/enemy-damaged" + str(self.direction) + ".png"
            self.enemy_file = PhotoImage(file=self.current_image_file)
            self.canvas.itemconfig(self.enemy, image=self.enemy_file)
        Thread(target=self.__set_image_to_default).start()

    def __set_image_to_default(self) -> None:
        """
        resets image to default
        """

        sleep(0.2)
        if not self.current_image_file == "resource-packs/" + self.resource_pack + "/enemy/movement/enemy" + str(self.direction) + ".png":
            self.dont_change_image_protocol = False
            self.current_image_file = "resource-packs/" + self.resource_pack + "/enemy/movement/enemy" + str(self.direction) + ".png"
            self.enemy_file = PhotoImage(file=self.current_image_file)
            self.canvas.itemconfig(self.enemy, image=self.enemy_file)

    # noinspection PyCompatibility
    def auto_move(self) -> None:
        """
        automatically moves enemy against player
        """

        self.move_to_x: int = 0
        self.move_to_y = 0

        while self.health > 0 and self.game_running:
            while self.player.is_game_paused:
                sleep(0.2)

            if self.player.health <= 0:
                break

            self.__attack_player()
            sleep(0.01)

            x = 0
            y = 0

            if self.player.invisible:
                if self.move_to_x - self.player.movement <= self.player.x <= self.move_to_x + self.player.movement and self.move_to_y - self.player.movement <= self.player.y <= self.move_to_y + self.player.movement:
                    self.move_to_y = randint(10, 1070)
                    self.move_to_x = randint(10, 1910)
            else:
                self.move_to_x = self.player.x
                self.move_to_y = self.player.y

            if self.x > self.move_to_x:
                x -= 1
                self.direction = 3

            elif self.x < self.move_to_x:
                x += 1
                self.direction = 1

            if self.y > self.move_to_y:
                y -= 1
                self.direction = 0

            elif self.y < self.move_to_y:
                y += 1
                self.direction = 2

            self.y += y
            self.x += x

            self.canvas.move(self.enemy, x, y)
            if not self.current_image_file == "resource-packs/" + self.resource_pack + "/enemy/movement/enemy" + str(self.direction) + ".png" and not self.dont_change_image_protocol:
                self.current_image_file = "resource-packs/" + self.resource_pack + "/enemy/movement/enemy" + str(self.direction) + ".png"
                self.enemy_file = PhotoImage(file=self.current_image_file)
                self.canvas.itemconfig(self.enemy, image=self.enemy_file)

        if self.health <= 0:
            self.__start_die_animation()
            sleep(self.despawn_timer)

        self.__delete()

    def __start_die_animation(self) -> None:
        """
        starts die animation
        """

        if not self.current_image_file == "resource-packs/" + self.resource_pack + "/enemy/enemy-dead.png":
            self.dont_change_image_protocol = True
            self.current_image_file = "resource-packs/" + self.resource_pack + "/enemy/enemy-dead.png"
            self.enemy_file = PhotoImage(file=self.current_image_file)
            self.canvas.itemconfig(self.enemy, image=self.enemy_file)

    def __delete(self) -> None:
        """
        deletes enemy image from tkinter
        """

        self.canvas.delete(self.enemy)


if __name__ == '__main__':
    pass
