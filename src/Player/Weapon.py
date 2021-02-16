from math import sqrt, floor

from Player.Player import *


class Weapon:
    def __init__(self, player, weapon_name: str, weapon_damage: int = 10, weapon_fire_rate: int = 2):
        self.player = player
        self.canvas = self.player.canvas

        self.weapon_name = weapon_name
        self.weapon_damage = weapon_damage
        self.weapon_fire_rate = weapon_fire_rate

    def get_bullet_track(self, x1, y1):
        x2 = self.player.x
        y2 = self.player.y
        x3 = x1 * (y2 / y1)
        c2 = sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))
        c1 = sqrt((y1 ** 2) + (x3 ** 2))

        os_x = x3
        index = 0
        pixel_coordinates = []
        ratio = y2 / x3
        while index != os_x:
            pixel_coordinates.append([index, floor(index * ratio)])
            index += 1

        return pixel_coordinates


if __name__ == '__main__':
    pass
