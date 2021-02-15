from src.Global_Functions import *


class Player:
    def __init__(self, canvas: Canvas, start_health: int = 100, x: int = 1920 / 2, y: int = 1080 / 2, movement: int = 10) -> None:
        self.direction = UP
        self.health = start_health
        self.movement = movement
        self.x = x
        self.y = y

        self.canvas = canvas
        self.sprite_file = PhotoImage(file="img/entities/player.png")
        self.sprite = self.canvas.create_image(self.x, self.y, anchor=N, image=self.sprite_file)

        listener = PlayerListener(self, self.canvas)
        Thread(target=listener.join).start()

        self.knife_attack_running = False
        self.knife_damage = 25
        self.knife_attack_speed = 2

        self.flick_recharge_time = 5
        self.flick_recharging = False
        self.flick_distance = 150

        self.enemies = []
        self.game_paused = False

        self.health_label = canvas.create_text(1840, 20, font="Normal 20 normal normal",
                                               text="Health: " + str(self.health))
        self.knife_attack_speed_label = canvas.create_text(1820, 50, font="Normal 14 normal normal",
                                                           text="Knife attack speed: " + str(self.knife_attack_speed))
        self.knife_damage_label = canvas.create_text(1840, 80, font="Normal 14 normal normal",
                                                     text="Knife damage: " + str(self.knife_damage))
        self.flick_recharge_label = canvas.create_text(1800, 110, font="Normal 14 normal normal",
                                                       text="Flick: READY")

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

    def attack_with_knife(self) -> None:
        if self.knife_attack_running:
            return None

        self.knife_attack_running = True
        x = self.x
        y = self.y
        rotation = 0

        if self.direction == UP:
            y -= 50
            rotation = 90
        elif self.direction == RIGHT:
            x += 50
            rotation = 270
        elif self.direction == DOWN:
            y += 50
            rotation = 180
        elif self.direction == LEFT:
            x -= 50
            rotation = 0

        knife_file = PhotoImage(file="img/knife/knife" + str(rotation) + ".png")
        self.canvas.image = knife_file
        knife = self.canvas.create_image(x, y, anchor=N, image=knife_file)
        Thread(target=self.delete_knife, args=(knife, 0.25)).start()

        for enemy in self.enemies:
            if enemy.x - 50 < x < enemy.x + 50 and enemy.y - 50 < y < enemy.y + 50:
                enemy.take_damage(self.knife_damage)

    def delete_knife(self, knife_number: int, timeout: int = 0.25) -> None:
        while self.game_paused:
            sleep(1)

        sleep(timeout)
        self.canvas.delete(knife_number)
        sleep((1 / self.knife_attack_speed) - timeout)
        self.knife_attack_running = False

    def flick(self) -> None:
        if self.flick_recharging:
            return None

        x = 0
        y = 0

        if self.direction == UP:
            y -= self.flick_distance
        elif self.direction == RIGHT:
            x += self.flick_distance
        elif self.direction == DOWN:
            y += self.flick_distance
        elif self.direction == LEFT:
            x -= self.flick_distance

        self.x += x
        self.y += y

        self.canvas.move(self.sprite, x, y)

        self.flick_recharging = True
        self.canvas.itemconfig(self.flick_recharge_label, text="Flick: Not Ready")
        Thread(target=self.recharge_flick).start()

    def recharge_flick(self):
        while self.game_paused:
            sleep(1)

        slept = 0
        while slept <= self.flick_recharge_time:
            while self.game_paused:
                sleep(1)
            sleep(1)
            self.canvas.itemconfig(self.flick_recharge_label,
                                   text="Flick: Ready in " + str(self.flick_recharge_time - slept) + " seconds...")
            slept += 1
        self.flick_recharging = False
        self.canvas.itemconfig(self.flick_recharge_label,
                               text="Flick: READY")

    def start_die_animation(self) -> None:
        while self.game_paused:
            sleep(1)

        for enemy in self.enemies:
            enemy.game_running = False

        self.canvas.unbind_all("<Key>")
        self.sprite_file = PhotoImage(file="img/entities/player-dead.png")
        self.canvas.itemconfig(self.sprite, image=self.sprite_file)

    def take_damage(self, damage: int) -> None:
        while self.game_paused:
            sleep(1)

        self.health -= damage
        self.canvas.itemconfig(self.health_label, text="Health: " + str(self.health))
        if self.health == 0:
            self.start_die_animation()
            return None

        self.sprite_file = PhotoImage(file="img/entities/entity-damaged.png")
        self.canvas.itemconfig(self.sprite, image=self.sprite_file)
        Thread(target=self.set_image_to_default).start()

    def set_image_to_default(self) -> None:
        while self.game_paused:
            sleep(1)

        sleep(0.2)
        self.sprite_file = PhotoImage(file="img/entities/player.png")
        self.canvas.itemconfig(self.sprite, image=self.sprite_file)
        if self.health == 0:
            self.start_die_animation()


class PlayerListener:
    def __init__(self, player: Player, canvas: Canvas) -> None:
        self.player = player
        self.canvas = canvas

    def on_press(self, event: any) -> None:
        if self.player.game_paused:
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
            self.player.attack_with_knife()
        elif key == "f":
            self.player.flick()

    def join(self) -> None:
        self.canvas.bind_all("<Key>", self.on_press)


if __name__ == '__main__':
    pass
