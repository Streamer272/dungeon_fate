from tkinter import *
from time import sleep
from threading import Thread
from math import floor

from Global_Functions import *
from Player import *


class Dash:
    def __init__(self, canvas: Canvas, player, dash_distance: int = 250, dash_recharge_time: int = 5, dash_damage: int = 50):
        self.canvas = canvas
        self.player = player

        self.player.movement += 10
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

        # for everyone reading this code, its a bug in tkinter, so we cant use for loop because the animation
        # wont play right, so we need to do this
        # dash_to_x1 = floor(self.player.x + (x / 3) * 1)
        # dash_to_y1 = floor(self.player.y + (y / 3) * 1)
        # dash_to_x2 = floor(self.player.x + (x / 3) * 2)
        # dash_to_y2 = floor(self.player.y + (y / 3) * 2)
        # dash_to_x3 = floor(self.player.x + (x / 3) * 3)
        # dash_to_y3 = floor(self.player.y + (y / 3) * 3)
        # Thread(target=self.move, args=[dash_to_x1, dash_to_y1, 0]).start()
        # Thread(target=self.move, args=[dash_to_x2, dash_to_y2, 0.05]).start()
        # Thread(target=self.move, args=[dash_to_x3, dash_to_y3, 0.1]).start()

        for i in range(floor(self.dash_distance / 50)):
            dash_to_x = floor(self.player.x + (x / (self.dash_distance / 50)) * (i + 1))
            dash_to_y = floor(self.player.y + (y / (self.dash_distance / 50)) * (i + 1))
            Thread(target=self.move, args=[dash_to_x, dash_to_y, 0.05 * (i + 1)]).start()

        self.player.x += x
        self.player.y += y

    def move(self, x: int, y: int, timeout: float = 0):
        sleep(timeout)
        self.canvas.coords(self.player.sprite, x, y)

        for enemy in self.player.enemies:
            if enemy.x - 50 < x < enemy.x + 50 and enemy.y - 50 < y < enemy.y + 50:
                enemy.take_damage(self.dash_damage)
                if enemy.health <= 0:
                    self.player.operator.on_enemy_killed()

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
