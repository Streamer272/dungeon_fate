from random import randint, choice

from Player.Player import *


class Enemy:
    def __init__(self, canvas: Canvas, player: Player, health: int = 50, damage: int = 10,
                 attack_speed: float = 0.5) -> None:
        self.player = player
        self.health = health
        self.game_running = True
        self.despawn_timer = 10

        self.damage = damage
        self.charging_attack = False
        self.attack_speed = attack_speed

        self.x, self.y = self.generate_spawn_position()

        self.canvas = canvas
        self.enemy_file = PhotoImage(file="img/entities/enemy.png")
        self.enemy = self.canvas.create_image(self.x, self.y, anchor=N, image=self.enemy_file)

    def generate_spawn_position(self):
        x_possible = [[self.player.x - 500, self.player.x - 250], [self.player.x + 250, self.player.x + 500]]
        y_possible = [[self.player.y - 500, self.player.y - 250], [self.player.y + 250, self.player.y + 500]]
        x_choice = choice(x_possible)
        y_choice = choice(y_possible)
        x = randint(x_choice[0], x_choice[1])
        y = randint(y_choice[0], y_choice[1])

        if x < 0 or y < 0 or x > 1920 or y > 1080:
            x, y = self.generate_spawn_position()

        if x % 5 != 0 or y % 5 != 0:
            x, y = self.generate_spawn_position()

        return x, y

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
        Thread(target=self.set_image_to_default).start()

    def set_image_to_default(self) -> None:
        sleep(0.2)
        self.enemy_file = PhotoImage(file="img/entities/enemy.png")
        self.canvas.itemconfig(self.enemy, image=self.enemy_file)

    def auto_move(self) -> None:
        while self.health > 0 and self.game_running:
            self.attack_enemy()
            sleep(0.01)

            x = 0
            y = 0

            if self.x > self.player.x:
                x -= 1

            elif self.x < self.player.x:
                x += 1

            if self.y > self.player.y:
                y -= 1

            elif self.y < self.player.y:
                y += 1

            self.y += y
            self.x += x

            self.canvas.move(self.enemy, x, y)

        if self.health <= 0:
            self.die()
            sleep(self.despawn_timer)
        self.destroy()

    def die(self) -> None:
        self.enemy_file = PhotoImage(file="img/entities/enemy-dead.png")
        self.canvas.itemconfig(self.enemy, image=self.enemy_file)

    def destroy(self) -> None:
        self.canvas.delete(self.enemy)


if __name__ == '__main__':
    pass
