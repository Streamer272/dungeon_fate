from json import loads

from src.Enemy.Enemy import *


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

    def add_enemies(self):
        waves = loads(open("waves.json", "r").read())
        for wave in waves:
            for i in range(3):
                say(self.canvas, text=wave["name"] + " is coming in " + str(3 - i) + "...", timeout=1)
                sleep(1)

            enemies = []
            for i in range(wave["enemy-count"]):
                if self.player.health != 0:
                    enemy = Enemy(self.canvas, self.player, wave["enemy"]["health"], wave["enemy"]["damage"], wave["enemy"]["attack-speed"])
                    self.player.enemies.append(enemy)
                    enemies.append(enemy)
                    Thread(target=enemy.auto_move).start()
                    sleep(wave["spawn-timeout"])


if __name__ == "__main__":
    gui = Gui()
    gui.create()
