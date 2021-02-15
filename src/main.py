from Enemy import *


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

    def add_enemies(self, count: int = 10, timeout: int = 3):
        say(self.canvas, text="First wave is coming in 3 seconds...", timeout=3)
        sleep(3)
        for i in range(count):
            if self.player.health != 0:
                enemy = Enemy(self.canvas, self.player, 50, 10, 2)
                self.player.enemies.append(enemy)
                Thread(target=enemy.auto_move).start()
                sleep(timeout)


if __name__ == "__main__":
    gui = Gui()
    gui.create()
