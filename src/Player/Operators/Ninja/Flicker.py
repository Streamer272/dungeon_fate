from tkinter import *
from time import sleep
from threading import Thread

from Global_Functions import *
from Player import *


class Flicker:
    def __init__(self, canvas: Canvas, player, flick_distance: int = 250, flick_recharge_time: int = 5):
        self.canvas = canvas
        self.player = player

        self.player.movement += 5
        self.flick_distance = flick_distance
        self.flick_recharge_time = flick_recharge_time
        self.is_flick_recharging = False

        self.flick_recharge_label = self.canvas.create_text(1800, 110, font="Normal 14 normal normal",
                                                            text="Flick: READY")

    def use(self) -> None:
        if self.is_flick_recharging:
            return None

        x = 0
        y = 0

        if self.player.direction == UP:
            y -= self.flick_distance
        elif self.player.direction == RIGHT:
            x += self.flick_distance
        elif self.player.direction == DOWN:
            y += self.flick_distance
        elif self.player.direction == LEFT:
            x -= self.flick_distance

        self.player.x += x
        self.player.y += y

        self.canvas.move(self.player.sprite, x, y)

        self.is_flick_recharging = True
        self.canvas.itemconfig(self.flick_recharge_label, text="Flick: Not Ready")
        Thread(target=self.recharge_flick).start()

    def recharge_flick(self):
        while self.player.is_game_paused:
            sleep(1)

        slept = 0
        while slept <= self.flick_recharge_time:
            while self.player.is_game_paused:
                sleep(1)
            sleep(1)
            self.canvas.itemconfig(self.flick_recharge_label,
                                   text="Flick: Ready in " + str(self.flick_recharge_time - slept) + " seconds...")
            slept += 1

        self.is_flick_recharging = False
        self.canvas.itemconfig(self.flick_recharge_label,
                               text="Flick: READY")


if __name__ == "__main__":
    pass
