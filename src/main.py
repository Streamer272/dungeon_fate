from json import loads

from Enemy.Enemy import *


class Gui:
    player: Player
    canvas: Canvas
    win: Tk

    def create(self) -> None:
        self.win = Tk()
        self.win.title("2D Game")
        self.win.attributes('-fullscreen', True)

        self.canvas = Canvas(self.win, height=1080, width=1920, bg="white")
        self.canvas.pack()

        self.player = Player(self.canvas, 100)
        Thread(target=self.add_enemies).start()

        self.win.mainloop()

    @staticmethod
    def check_enemies_health(enemies: list) -> bool:
        dead_enemies = 0
        for enemy in enemies:
            if enemy.health <= 0:
                dead_enemies += 1

        return dead_enemies == len(enemies)

    def add_enemies(self) -> None:
        waves = loads(open("waves.json", "r").read())
        for wave in waves:
            enemies = []
            self.player.enemies = []

            for i in range(3):
                say(self.canvas, text=wave["name"] + " is coming in " + str(3 - i) + "...", timeout=1)
                sleep(1)

            for i in range(wave["enemy-count"]):
                if self.player.health == 0:
                    return None

                enemy = Enemy(self.canvas, self.player, wave["enemy"]["health"], wave["enemy"]["damage"], wave["enemy"]["attack-speed"])
                self.player.enemies.append(enemy)
                enemies.append(enemy)
                Thread(target=enemy.auto_move).start()
                sleep(wave["spawn-timeout"])

            while not self.check_enemies_health(enemies):
                sleep(1)

        say(self.canvas, text="Congratulations! You won!", timeout=10)
        self.player.is_game_paused = True
        sleep(10)


if __name__ == "__main__":
    gui = Gui()
    gui.create()
