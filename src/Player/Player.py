from tkinter import *
from threading import Thread
from time import sleep
from pynput.keyboard import Key, Listener
from keyboard import is_pressed

from Player.Weapons.Knife import *
from Player.Weapons.Weapon import *
from Global_Functions import *

from Player.Operators.Ninja.Dash import *
from Player.Operators.Ghost.Ghost import *


class Player:
    def __init__(self, canvas: Canvas, resource_pack_name: str, operator: str, health: int = 100, x: int = 1920 / 2, y: int = 1080 / 2, movement: int = 10) -> None:
        self.direction = UP
        self.health = health
        self.invisible = False
        self.dont_take_damage_protocol = False

        self.is_moving = False
        self.max_steps_per_second = 25
        self.movement = movement
        self.x = x
        self.y = y

        self.canvas = canvas
        self.resource_pack = resource_pack_name
        self.dont_change_image_protocol = False
        self.current_image_file = "resource-packs/" + self.resource_pack + "/player/movement/player" + str(self.direction) + ".png"
        self.sprite_file = PhotoImage(file=self.current_image_file)
        self.sprite = self.canvas.create_image(self.x, self.y, anchor=N, image=self.sprite_file)

        self.knife = Knife(self, 25, 1)

        self.operator = operator
        if self.operator == "Ninja":
            self.operator = Dash(self, 250, 5)
        elif self.operator == "Ghost":
            self.operator = Ghost(self, 3, 10)
        else:
            self.operator = Dash(self, 250, 5)

        self.enemies = []
        self.is_game_paused = False

        listener = PlayerListener(self, self.canvas)
        Thread(target=listener.join).start()

        self.health_label = canvas.create_text(1840, 20, font="Normal 20 normal normal",
                                               text="Health: " + str(self.health))

    def move(self, direction: int, steps: int) -> None:
        if self.is_moving:
            return None
        self.is_moving = True

        x = 0
        y = 0

        if direction == UP:
            if self.y - steps <= 0:
                return None

            y -= steps
        elif direction == RIGHT:
            if self.x + steps >= 1900:
                return None

            x += steps
        elif direction == DOWN:
            if self.y + steps >= 1030:
                return None

            y += steps
        elif direction == LEFT:
            if self.x - steps <= 20:
                return None

            x -= steps

        self.x += x
        self.y += y

        self.direction = direction
        self.canvas.move(self.sprite, x, y)
        if not self.current_image_file == "resource-packs/" + self.resource_pack + "/player/movement/player" + str(self.direction) + ".png" and not self.dont_change_image_protocol:
            self.current_image_file = "resource-packs/" + self.resource_pack + "/player/movement/player" + str(self.direction) + ".png"
            self.sprite_file = PhotoImage(file=self.current_image_file)
            self.canvas.itemconfig(self.sprite, image=self.sprite_file)

        Thread(target=self.after_move).start()

    def after_move(self):
        sleep(1 / self.max_steps_per_second)
        self.is_moving = False

    def start_die_animation(self) -> None:
        while self.is_game_paused:
            sleep(1)

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
        while self.is_game_paused:
            sleep(1)

        if self.health >= 0:
            pass

        if self.invisible or self.dont_take_damage_protocol:
            return None

        self.health -= damage
        self.canvas.itemconfig(self.health_label, text="Health: " + str(self.health))
        if self.health <= 0:
            self.start_die_animation()
            return None

        self.operator.on_take_damage()

        if not self.current_image_file == "resource-packs/" + self.resource_pack + "/player/damaged/player-damaged" + str(self.direction) + ".png" and not self.dont_change_image_protocol:
            self.dont_change_image_protocol = True
            self.current_image_file = "resource-packs/" + self.resource_pack + "/player/damaged/player-damaged" + str(self.direction) + ".png"
            self.sprite_file = PhotoImage(file=self.current_image_file)
            self.canvas.itemconfig(self.sprite, image=self.sprite_file)
        Thread(target=self.set_image_to_default).start()

    def set_image_to_default(self) -> None:
        while self.is_game_paused:
            sleep(1)

        sleep(0.2)
        if not self.current_image_file == "resource-packs/" + self.resource_pack + "/player/movement/player" + str(self.direction) + ".png":
            self.dont_change_image_protocol = False
            self.current_image_file = "resource-packs/" + self.resource_pack + "/player/movement/player" + str(self.direction) + ".png"
            self.sprite_file = PhotoImage(file=self.current_image_file)
            self.canvas.itemconfig(self.sprite, image=self.sprite_file)
        if self.health == 0:
            self.start_die_animation()


class PlayerListener:
    def __init__(self, player: Player, canvas: Canvas) -> None:
        self.player = player
        self.canvas = canvas

    def on_press(self, key: str) -> None:
        if self.player.is_game_paused:
            return None

        if key == "w":
            Thread(target=self.player.move, args=[UP, self.player.movement]).start()
        elif key == "d":
            Thread(target=self.player.move, args=[RIGHT, self.player.movement]).start()
        elif key == "s":
            Thread(target=self.player.move, args=[DOWN, self.player.movement]).start()
        elif key == "a":
            Thread(target=self.player.move, args=[LEFT, self.player.movement]).start()
        elif key == "e":
            Thread(target=self.player.knife.attack_with_knife, args=[]).start()
        elif key == "f":
            Thread(target=self.player.operator.use, args=[]).start()

    def join(self) -> None:
        while True:
            while self.player.is_game_paused:
                sleep(1)

            if is_pressed("w"):
                self.on_press("w")
            elif is_pressed("d"):
                self.on_press("d")
            elif is_pressed("s"):
                self.on_press("s")
            elif is_pressed("a"):
                self.on_press("a")
            if is_pressed("e"):
                self.on_press("e")
            if is_pressed("f"):
                self.on_press("f")

            sleep(1 / self.player.max_steps_per_second)


if __name__ == '__main__':
    pass
