"""
player file
"""

from tkinter import *
from threading import Thread
from time import sleep
from src.external_libraries import keyboard
from src.external_libraries import mouse

from src.Player.Weapons.Knife import *
from src.Player.Weapons.Weapon import *
from src.GlobalFunctions import *
from src.AccountController import *

from src.Player.Operators.Ninja.Dash import *
from src.Player.Operators.Ghost.Ghost import *
from src.Player.Operators.Wizard.Wizard import *


class Player:
    """
    player controller
    """

    def __init__(self, gui, health: int = 100, x: int = 1920 / 2,
                 y: int = 1080 / 2, movement: int = 10) -> None:
        self.direction = D_UP
        self.health = health
        self.invisible = False
        self.dont_take_damage_protocol = False

        self.is_moving = False
        self.max_steps_per_second = 25
        self.movement = movement
        self.x = x
        self.y = y

        self.gui = gui
        self.canvas = self.gui.canvas
        self.resource_pack = self.gui.resource_pack.get()
        self.dont_change_image_protocol = False

        self.current_image_file = "resource-packs/" + self.resource_pack + "/player/movement/player" + str(
            self.direction) + ".png"
        self.sprite_file = PhotoImage(file=self.current_image_file)
        self.sprite = self.canvas.create_image(self.x, self.y, anchor=N, image=self.sprite_file)

        self.knife = Knife(self)

        self.operator = self.gui.operator.get()
        if self.operator == "Ninja":
            self.operator = Dash(self)
        elif self.operator == "Ghost":
            self.operator = Ghost(self)
        elif self.operator == "Wizard":
            self.operator = Wizard(self)
        else:
            self.operator = Dash(self)

        self.enemies = []
        self.is_game_paused = False
        self.pistol = Weapon(self)

        self.listener = PlayerListener(self, self.canvas)
        Thread(target=self.listener.join).start()

        self.health_label = self.canvas.create_text(1840, 20, font="Normal 20 normal normal",
                                                    text="Health: " + str(self.health))

    def __del__(self):
        self.resume_game()
        self.listener.leave()
        del self.listener
        self.canvas.delete(self.sprite)

    def pause_game(self) -> None:
        """
        pauses game
        """

        self.is_game_paused = True

        self.pause_game_text_id = alert(self.canvas, text="Game Paused", timeout=None)

    def resume_game(self) -> None:
        """
        resumes game
        """

        self.is_game_paused = False

        try:
            self.canvas.delete(self.pause_game_text_id)
        except NameError:
            pass

    def move(self, direction: int, steps: int) -> None:
        """
        moves player
        :param direction:
        :param steps:
        :return: Nonetype
        """

        if self.is_moving:
            return None

        x = 0
        y = 0

        if direction == D_UP:
            if self.y - steps - 1 <= 0:
                return None

            y -= steps

        elif direction == D_RIGHT:
            if self.x + steps + 1 >= 1890:
                return None

            x += steps

        elif direction == D_DOWN:
            if self.y + steps + 1 >= 1030:
                return None

            y += steps

        elif direction == D_LEFT:
            if self.x - steps - 1 <= 30:
                return None

            x -= steps

        self.is_moving = True
        self.x += x
        self.y += y

        self.direction = direction
        self.canvas.move(self.sprite, x, y)
        if not self.current_image_file == "resource-packs/" + self.resource_pack + "/player/movement/player" + str(
                self.direction) + ".png" and not self.dont_change_image_protocol:
            self.current_image_file = "resource-packs/" + self.resource_pack + "/player/movement/player" + str(
                self.direction) + ".png"
            self.sprite_file = PhotoImage(file=self.current_image_file)
            self.canvas.itemconfig(self.sprite, image=self.sprite_file)

        Thread(target=self.__after_move).start()

    def __after_move(self):
        sleep(1 / self.max_steps_per_second)
        self.is_moving = False

    def __start_die_animation(self) -> None:
        while self.is_game_paused:
            sleep(0.2)

        for enemy in self.enemies:
            enemy.game_running = False

        self.operator.on_player_dead()

        if self.health <= 0:
            self.is_game_paused = True
            if not self.current_image_file == "resource-packs/" + self.resource_pack + "/player/player-dead.png":
                self.dont_change_image_protocol = True
                self.current_image_file = "resource-packs/" + self.resource_pack + "/player/player-dead.png"
                self.sprite_file = PhotoImage(file=self.current_image_file)
                self.canvas.itemconfig(self.sprite, image=self.sprite_file)

    def take_damage(self, damage: int) -> None:
        """
        take damage from any source
        :param damage:
        :return: Nonetype
        """

        while self.is_game_paused:
            sleep(0.2)

        if self.health <= 0:
            return None

        if self.invisible or self.dont_take_damage_protocol:
            return None

        self.health -= damage
        self.operator.on_take_damage(damage)
        self.canvas.itemconfig(self.health_label, text="Health: " + str(self.health))

        if self.health <= 0:
            self.__start_die_animation()
            return None

        if not self.current_image_file == "resource-packs/" + self.resource_pack + "/player/damaged/player-damaged" + str(
                self.direction) + ".png" and not self.dont_change_image_protocol:
            self.dont_change_image_protocol = True
            self.current_image_file = "resource-packs/" + self.resource_pack + "/player/damaged/player-damaged" + str(
                self.direction) + ".png"
            self.sprite_file = PhotoImage(file=self.current_image_file)
            self.canvas.itemconfig(self.sprite, image=self.sprite_file)
        Thread(target=self.__set_image_to_default).start()

    def __set_image_to_default(self) -> None:
        while self.is_game_paused:
            sleep(0.2)

        sleep(0.2)
        if not self.current_image_file == "resource-packs/" + self.resource_pack + "/player/movement/player" + str(
                self.direction) + ".png":
            self.dont_change_image_protocol = False
            self.current_image_file = "resource-packs/" + self.resource_pack + "/player/movement/player" + str(
                self.direction) + ".png"
            self.sprite_file = PhotoImage(file=self.current_image_file)
            self.canvas.itemconfig(self.sprite, image=self.sprite_file)
        if self.health <= 0:
            self.__start_die_animation()


class PlayerListener:
    """
    player listener controller
    """

    def __init__(self, player: Player, canvas: Canvas) -> None:
        self.player = player
        self.canvas = canvas

        self.listen = True

    def __del__(self):
        self.leave()

    def __on_press(self, key: str) -> None:
        if self.player.is_game_paused:
            return None

        if key == "w":
            Thread(target=self.player.move, args=[D_UP, self.player.movement]).start()
        elif key == "d":
            Thread(target=self.player.move, args=[D_RIGHT, self.player.movement]).start()
        elif key == "s":
            Thread(target=self.player.move, args=[D_DOWN, self.player.movement]).start()
        elif key == "a":
            Thread(target=self.player.move, args=[D_LEFT, self.player.movement]).start()
        elif key == "e":
            Thread(target=self.player.knife.attack_with_knife, args=[]).start()
        elif key == "f":
            Thread(target=self.player.operator.use, args=[]).start()

    def __toggle_pause(self) -> None:
        if self.player.is_game_paused:
            Thread(target=self.player.resume_game()).start()
        else:
            Thread(target=self.player.pause_game()).start()

    def __shoot_bullet(self, position: tuple) -> None:
        if self.player.is_game_paused or not self.listen:
            return None

        try:
            Thread(target=self.player.pistol.shoot_bullet, args=[position[0], position[1]]).start()

        except TypeError:
            pass

    def __pass__(self) -> None:
        pass

    def join(self) -> None:
        """
        starts listener
        """

        mouse.on_click(lambda: self.__shoot_bullet(mouse.get_position()))
        self.canvas.bind_all("<Escape>", lambda event: self.__toggle_pause())

        while self.listen:
            while self.player.is_game_paused:
                sleep(0.2)

            if keyboard.is_pressed("w"):
                Thread(target=self.__on_press, args=["w"]).start()
            elif keyboard.is_pressed("d"):
                Thread(target=self.__on_press, args=["d"]).start()
            elif keyboard.is_pressed("s"):
                Thread(target=self.__on_press, args=["s"]).start()
            elif keyboard.is_pressed("a"):
                Thread(target=self.__on_press, args=["a"]).start()
            if keyboard.is_pressed("e"):
                Thread(target=self.__on_press, args=["e"]).start()
            if keyboard.is_pressed("f"):
                Thread(target=self.__on_press, args=["f"]).start()

            sleep(1 / self.player.max_steps_per_second)

        self.canvas.unbind_all("<Escape>")
        mouse.on_click(lambda: self.__pass__())

    def leave(self) -> None:
        """
        stops listener
        """

        self.listen = False


if __name__ == '__main__':
    pass
