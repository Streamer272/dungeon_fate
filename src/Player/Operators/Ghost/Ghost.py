"""
ghost file
"""

from tkinter import *
from time import sleep
from threading import Thread

from src.GlobalFunctions import *
from src.Player import *


class Ghost:
    """
    ghost controller
    """

    def __init__(self, player, ghost_duration: int = 3, ghost_recharge_time: int = 10) -> None:
        self.canvas = player.canvas
        self.player = player

        self.ghost_duration = ghost_duration
        self.ghost_recharge_time = ghost_recharge_time
        self.is_ghost_recharging = False

        self.passive_duration = 1
        self.passive_recharge_time = 5
        self.is_passive_recharging = False

        self.ghost_recharge_label = self.canvas.create_text(1800, 110, font="Normal 14 normal normal",
                                                            text="Ghost: READY")
        self.passive_recharge_label = self.canvas.create_text(1800, 140, font="Normal 14 normal normal",
                                                              text="Passive: READY")

    def use(self) -> None:
        Thread(target=self.__use_ghost).start()

    def __use_ghost(self) -> None:
        if self.is_ghost_recharging:
            return None
        self.canvas.itemconfig(self.ghost_recharge_label, text="Ghost: Using")

        self.player.invisible = True
        sleep(self.ghost_duration)
        self.player.invisible = False
        self.is_ghost_recharging = True

        self.canvas.itemconfig(self.ghost_recharge_label, text="Ghost: Not Ready")
        Thread(target=self.__recharge_ghost).start()

    def __recharge_ghost(self) -> None:
        while self.player.is_game_paused:
            sleep(1)

        slept = 0
        while slept < self.ghost_recharge_time:
            while self.player.is_game_paused:
                sleep(1)
            sleep(1)
            self.canvas.itemconfig(self.ghost_recharge_label,
                                   text="Ghost: Ready in " + str(self.ghost_recharge_time - slept) + " seconds...")
            slept += 1

        self.is_ghost_recharging = False
        self.canvas.itemconfig(self.ghost_recharge_label, text="Ghost: READY")

    def __use_passive(self) -> None:
        if self.is_passive_recharging or self.player.invisible:
            return None

        self.canvas.itemconfig(self.passive_recharge_label, text="Passive: Using")

        self.player.invisible = True
        sleep(self.passive_duration)
        self.player.invisible = False
        self.is_passive_recharging = True

        self.canvas.itemconfig(self.passive_recharge_label, text="Passive: Not Ready")
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

    def on_player_dead(self) -> None:
        """
        on player dead
        """

        pass

    def on_enemy_killed(self) -> None:
        """
        on enemy killed
        """

        pass

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
