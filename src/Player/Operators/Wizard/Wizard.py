"""
wizard file
"""

from tkinter import *
from time import sleep
from threading import Thread

from src.GlobalFunctions import *
from src.Player import *


class Wizard:
    def __init__(self, player, active_recharge_time: int = 30, passive_recharge_time: int = 10) -> None:
        self.canvas = player.canvas
        self.player = player

        self.teleport_recharge_time = active_recharge_time
        self.dont_use_teleport_protocol = False
        self.is_teleport_recharging = False
        self.is_teleport_selection_active = False

        self.passive_recharge_time = passive_recharge_time
        self.is_passive_recharging = False

        self.teleport_recharge_label = self.canvas.create_text(1800, 110, font="Normal 14 normal normal",
                                                               text="Teleport: READY")
        self.passive_recharge_label = self.canvas.create_text(1800, 140, font="Normal 14 normal normal",
                                                              text="Passive: READY")

        self.canvas.bind_all("<Button-1>", self.__on_click)

    def use(self) -> None:
        Thread(target=self.__use_teleport).start()

    def __use_teleport(self) -> None:
        if self.is_teleport_recharging or self.dont_use_teleport_protocol:
            return None

        self.is_teleport_selection_active = not self.is_teleport_selection_active

        if self.is_teleport_selection_active:
            self.canvas.itemconfig(self.teleport_recharge_label, text="Teleport: Choosing location")
        else:
            self.canvas.itemconfig(self.teleport_recharge_label, text="Teleport: READY")

        self.dont_use_teleport_protocol = True
        Thread(target=self.__after_use_teleport).start()

    def __after_use_teleport(self) -> None:
        sleep(0.5)
        self.dont_use_teleport_protocol = False

    def __recharge_teleport(self) -> None:
        while self.player.is_game_paused:
            sleep(1)

        slept = 0
        while slept < self.teleport_recharge_time:
            while self.player.is_game_paused:
                sleep(1)
            sleep(1)
            self.canvas.itemconfig(self.teleport_recharge_label,
                                   text="Teleport: Ready in " + str(self.teleport_recharge_time - slept) + " seconds...")
            slept += 1

        self.is_teleport_recharging = False
        self.canvas.itemconfig(self.teleport_recharge_label, text="Teleport: READY")

    def __use_passive(self) -> None:
        if self.is_passive_recharging or self.player.health >= 100:
            return None

        self.canvas.itemconfig(self.passive_recharge_label, text="Passive: Using")

        self.player.health += 5
        self.canvas.itemconfig(self.player.health_label, text="Health: " + str(self.player.health))

        self.canvas.itemconfig(self.passive_recharge_label, text="Passive: Not Ready")
        self.is_passive_recharging = True
        Thread(target=self.__recharge_passive).start()

    def __recharge_passive(self) -> None:
        while self.player.is_game_paused:
            sleep(1)

        slept = 0
        while slept < self.passive_recharge_time:
            while self.player.is_game_paused:
                sleep(1)
            sleep(1)
            self.canvas.itemconfig(self.passive_recharge_label,
                                   text="Passive: Ready in " + str(self.passive_recharge_time - slept) + " seconds...")
            slept += 1

        self.is_passive_recharging = False
        self.canvas.itemconfig(self.passive_recharge_label, text="Passive: READY")

    def __on_click(self, event) -> None:
        if not self.is_teleport_selection_active:
            return None

        self.player.x = event.x
        self.player.y = event.y
        self.canvas.coords(self.player.sprite, self.player.x, self.player.y)

        self.is_teleport_recharging = True
        Thread(target=self.__recharge_teleport).start()

    def on_player_dead(self) -> None:
        """
        on player dead
        """

        pass

    def on_enemy_killed(self) -> None:
        """
        on enemy killed
        """

        Thread(target=self.__use_passive).start()

    def on_player_knife(self) -> None:
        """
        on player knife
        """

        pass

    def on_take_damage(self, damage: int) -> None:
        """
        on take damage
        :param damage:
        """

        pass


if __name__ == '__main__':
    pass
