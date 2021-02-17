from tkinter import *
from threading import Thread
from time import sleep

from Player.Knife import *
from Player.Flick import *
from Player.Weapon import *
from Global_Functions import *


class Player:
    def __init__(self, canvas: Canvas, resource_pack_name: str, health: int = 100, x: int = 1920 / 2, y: int = 1080 / 2, movement: int = 10) -> None:
        self.direction = UP
        self.health = health
        self.movement = movement
        self.x = x
        self.y = y

        self.canvas = canvas
        self.resource_pack = resource_pack_name
        self.dont_change_image_protocol = False
        self.current_image_file = "resource-packs/" + self.resource_pack + "/player/movement/player" + str(self.direction) + ".png"
        self.sprite_file = PhotoImage(file=self.current_image_file)
        self.sprite = self.canvas.create_image(self.x, self.y, anchor=N, image=self.sprite_file)

        listener = PlayerListener(self, self.canvas)
        Thread(target=listener.join).start()

        self.knife = Knife.Knife(self.canvas, self, 25, 1)
        self.flicker = Flicker(self.canvas, self, 250, 5)

        self.enemies = []
        self.is_game_paused = False

        self.health_label = canvas.create_text(1840, 20, font="Normal 20 normal normal",
                                               text="Health: " + str(self.health))

    def move(self, direction: int, steps: int) -> None:
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

    def start_die_animation(self) -> None:
        while self.is_game_paused:
            sleep(1)

        for enemy in self.enemies:
            enemy.game_running = False

        self.is_game_paused = True
        if not self.current_image_file == "resource-packs/" + self.resource_pack + "/player/player-dead.png":
            self.dont_change_image_protocol = True
            self.current_image_file = "resource-packs/" + self.resource_pack + "/player/player-dead.png"
            self.sprite_file = PhotoImage(file=self.current_image_file)
            self.canvas.itemconfig(self.sprite, image=self.sprite_file)

    def take_damage(self, damage: int) -> None:
        while self.is_game_paused:
            sleep(1)

        self.health -= damage
        self.canvas.itemconfig(self.health_label, text="Health: " + str(self.health))
        if self.health <= 0:
            self.start_die_animation()
            return None

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

    def on_press(self, event: any) -> None:
        if self.player.is_game_paused:
            return None

        key = str(event.char).lower()

        if key == "w":
            self.player.move(UP, self.player.movement)
        elif key == "d":
            self.player.move(RIGHT, self.player.movement)
        elif key == "s":
            self.player.move(DOWN, self.player.movement)
        elif key == "a":
            self.player.move(LEFT, self.player.movement)
        elif key == "e":
            self.player.knife.attack_with_knife()
        elif key == "f":
            self.player.flicker.flick()

    def join(self) -> None:
        self.canvas.bind_all("<Key>", self.on_press)


if __name__ == '__main__':
    pass
