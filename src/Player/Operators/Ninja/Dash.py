from tkinter import *
from time import sleep
from threading import Thread
from math import floor

from GlobalFunctions import *
from Player import *


class Dash:
    def __init__(self, player, dash_distance: int = 250, dash_recharge_time: int = 10, dash_damage: int = 50):
        self.canvas = player.canvas
        self.player = player

        self.player.movement *= 1.25
        self.dash_distance = dash_distance
        self.dash_recharge_time = dash_recharge_time
        self.dash_damage = dash_damage
        self.is_dash_recharging = False

        self.dash_recharge_label = self.canvas.create_text(1800, 110, font="Normal 14 normal normal",
                                                           text="Dash: READY")

    def use(self) -> None:
        Thread(target=self.use_dash).start()

    def use_dash(self) -> None:
        if self.is_dash_recharging:
            return None

        x = 0
        y = 0

        if self.player.direction == UP:
            y -= self.dash_distance
        elif self.player.direction == RIGHT:
            x += self.dash_distance
        elif self.player.direction == DOWN:
            y += self.dash_distance
        elif self.player.direction == LEFT:
            x -= self.dash_distance

        self.is_dash_recharging = True
        self.canvas.itemconfig(self.dash_recharge_label, text="Dash: Not Ready")
        Thread(target=self.recharge_dash).start()
        self.player.dont_take_damage_protocol = True

        for i in range(floor(self.dash_distance / 50)):
            dash_to_x = floor(self.player.x + (x / (self.dash_distance / 50)) * (i + 1))
            dash_to_y = floor(self.player.y + (y / (self.dash_distance / 50)) * (i + 1))
            Thread(target=self.move, args=[dash_to_x, dash_to_y, 0.05 * (i + 1)]).start()

        Thread(target=self.after_dash, args=[0.05 * floor(self.dash_distance / 50)]).start()

    def move(self, x: int, y: int, timeout: float = 0):
        if not (0 < x < 1920) or not (0 < y < 1080):
            return None

        sleep(timeout)
        self.canvas.coords(self.player.sprite, x, y)

        self.player.x = x
        self.player.y = y

        for enemy in self.player.enemies:
            if enemy.x - 50 < x < enemy.x + 50 and enemy.y - 50 < y < enemy.y + 50:
                enemy.take_damage(self.dash_damage)
                if enemy.health <= 0:
                    self.player.operator.on_enemy_killed()

    def after_dash(self, timeout: int):
        sleep(timeout + 0.5)
        self.player.dont_take_damage_protocol = False

    def recharge_dash(self):
        sleep(0.3)

        while self.player.is_game_paused:
            sleep(1)

        slept = 0
        while slept <= self.dash_recharge_time:
            while self.player.is_game_paused:
                sleep(1)
            sleep(1)
            self.canvas.itemconfig(self.dash_recharge_label,
                                   text="Dash: Ready in " + str(self.dash_recharge_time - slept) + " seconds...")
            slept += 1

        self.is_dash_recharging = False
        self.canvas.itemconfig(self.dash_recharge_label,
                               text="Dash: READY")

    def on_player_dead(self):
        pass

    def on_enemy_killed(self):
        pass

    def on_player_knife(self):
        pass

    def on_take_damage(self):
        pass


if __name__ == "__main__":
    pass
