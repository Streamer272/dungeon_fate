from tkinter import *
from time import sleep
from threading import Thread

from Global_Functions import *
from Player import *


class Ghost:
    def __init__(self, canvas: Canvas, player, ghost_duration: int = 3, ghost_recharge_time: int = 10):
        self.canvas = canvas
        self.player = player

        self.ghost_duration = ghost_duration
        self.ghost_recharge_time = ghost_recharge_time
        self.is_ghost_recharging = False

        self.ghost_recharge_label = self.canvas.create_text(1800, 110, font="Normal 14 normal normal",
                                                            text="Ghost: READY")

    def use(self) -> None:
        Thread(target=self.use_ghost).start()

    def use_ghost(self):
        if self.is_ghost_recharging:
            return None
        self.canvas.itemconfig(self.ghost_recharge_label, text="Ghost: Using")

        self.player.invisible = True
        sleep(self.ghost_duration)
        self.player.invisible = False
        self.is_ghost_recharging = True

        self.canvas.itemconfig(self.ghost_recharge_label, text="Ghost: Not Ready")
        Thread(target=self.recharge_ghost).start()

    def recharge_ghost(self):
        while self.player.is_game_paused:
            sleep(1)

        slept = 0
        while slept <= self.ghost_recharge_time:
            while self.player.is_game_paused:
                sleep(1)
            sleep(1)
            self.canvas.itemconfig(self.ghost_recharge_label,
                                   text="Ghost: Ready in " + str(self.ghost_recharge_time - slept) + " seconds...")
            slept += 1

        self.is_ghost_recharging = False
        self.canvas.itemconfig(self.ghost_recharge_label, text="Ghost: READY")


if __name__ == '__main__':
    pass
