from tkinter import *

from src.GlobalFunctions import *
from src.Player.Player import *


class Knife:
    def __init__(self, player, knife_damage: int = 25, knife_attack_speed: int = 1):
        self.canvas = player.canvas
        self.resource_pack = player.resource_pack
        self.player = player

        self.knife_damage = knife_damage
        self.is_player_knifing = False
        self.knife_attack_speed = knife_attack_speed

        self.knife_attack_speed_label = self.canvas.create_text(1820, 50, font="Normal 14 normal normal",
                                                                text="Knife attack speed: " + str(
                                                                    self.knife_attack_speed))
        self.knife_damage_label = self.canvas.create_text(1840, 80, font="Normal 14 normal normal",
                                                          text="Knife damage: " + str(self.knife_damage))

    def attack_with_knife(self) -> None:
        if self.is_player_knifing:
            return None

        self.is_player_knifing = True
        x = self.player.x
        y = self.player.y
        rotation = 0

        if self.player.direction == UP:
            y -= 50
            rotation = 0
        elif self.player.direction == RIGHT:
            x += 50
            rotation = 1
        elif self.player.direction == DOWN:
            y += 50
            rotation = 2
        elif self.player.direction == LEFT:
            x -= 50
            rotation = 3

        knife_file = PhotoImage(file="resource-packs/" + self.resource_pack + "/knife/knife" + str(rotation) + ".png")
        self.canvas.image = knife_file
        knife = self.canvas.create_image(x, y, anchor=N, image=knife_file)
        Thread(target=self.delete_knife, args=(knife, 0.25)).start()

        self.player.operator.on_player_knife()

        for enemy in self.player.enemies:
            if enemy.x - 50 < x < enemy.x + 50 and enemy.y - 50 < y < enemy.y + 50:
                enemy.take_damage(self.knife_damage)
                if enemy.health <= 0:
                    self.player.operator.on_enemy_killed()

    def delete_knife(self, knife_number: int, timeout: int = 0.25) -> None:
        while self.player.is_game_paused:
            sleep(1)

        sleep(timeout)
        self.canvas.delete(knife_number)
        sleep((1 / self.knife_attack_speed) - timeout)
        self.is_player_knifing = False


if __name__ == "__main__":
    pass
