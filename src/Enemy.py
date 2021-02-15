from random import randint

from Player import *


class Enemy:
    def __init__(self, canvas: Canvas, player: Player, start_health: int = 50, damage: int = 10, attack_speed: float = 0.5) -> None:
        self.player = player
        self.health = start_health
        self.game_running = True

        self.damage = damage
        self.charging_attack = False
        self.attack_speed = attack_speed

        self.x = randint(100, 1820)
        self.y = randint(100, 980)

        self.canvas = canvas
        self.enemy_file = PhotoImage(file="img/entities/enemy.png")
        self.enemy = self.canvas.create_image(self.x, self.y, anchor=N, image=self.enemy_file)

    def attack_enemy(self) -> None:
        if self.player.x - 50 < self.x < self.player.x + 50 and self.player.y - 50 < self.y < self.player.y + 50 and not self.charging_attack:
            self.player.take_damage(self.damage)
            self.charging_attack = True
            Thread(target=self.charge_attack).start()

    def charge_attack(self) -> None:
        sleep(1 / self.attack_speed)
        self.charging_attack = False

    def take_damage(self, damage: int) -> None:
        self.health -= damage
        self.enemy_file = PhotoImage(file="img/entities/entity-damaged.png")
        self.canvas.itemconfig(self.enemy, image=self.enemy_file)
        if self.health <= 0:
            self.die()
            return None
        Thread(target=self.change_image_back).start()

    def change_image_back(self) -> None:
        sleep(0.2)
        self.enemy_file = PhotoImage(file="img/entities/enemy.png")
        self.canvas.itemconfig(self.enemy, image=self.enemy_file)

    def auto_move(self) -> None:
        while self.health != 0 and self.game_running:
            self.attack_enemy()
            sleep(0.1)

            x = 0
            y = 0
            if self.x > self.player.x:
                x -= 5
            elif self.x < self.player.x:
                x += 5
            if self.y > self.player.y:
                y -= 5
            elif self.y < self.player.y:
                y += 5
            self.y += y
            self.x += x

            self.canvas.move(self.enemy, x, y)

        if self.health <= 0:
            self.die()
            sleep(2)
        self.destroy()

    def die(self) -> None:
        self.enemy_file = PhotoImage(file="img/entities/enemy-dead.png")
        self.canvas.itemconfig(self.enemy, image=self.enemy_file)

    def destroy(self) -> None:
        self.canvas.delete(self.enemy)


if __name__ == '__main__':
    pass
