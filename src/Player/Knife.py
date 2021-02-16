from tkinter import *
from Global_Functions import *
from Player import *


class Knife:
    def __init__(self, canvas: Canvas, player, knife_damage: int = 25, knife_attack_speed: int = 1):
        self.canvas = canvas
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
            rotation = 90
        elif self.player.direction == RIGHT:
            x += 50
            rotation = 270
        elif self.player.direction == DOWN:
            y += 50
            rotation = 180
        elif self.player.direction == LEFT:
            x -= 50
            rotation = 0

        knife_file = PhotoImage(file="img/knife/knife" + str(rotation) + ".png")
        self.canvas.image = knife_file
        knife = self.canvas.create_image(x, y, anchor=N, image=knife_file)
        Thread(target=self.delete_knife, args=(knife, 0.25)).start()

        for enemy in self.player.enemies:
            if enemy.x - 50 < x < enemy.x + 50 and enemy.y - 50 < y < enemy.y + 50:
                enemy.take_damage(self.knife_damage)

    def delete_knife(self, knife_number: int, timeout: int = 0.25) -> None:
        while self.player.game_paused:
            sleep(1)

        sleep(timeout)
        self.canvas.delete(knife_number)
        sleep((1 / self.knife_attack_speed) - timeout)
        self.is_player_knifing = False


if __name__ == "__main__":
    pass
