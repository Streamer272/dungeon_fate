from Player import *
from Directions import *


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

        self.win.mainloop()

    def do(self) -> None:
        self.player.move(self.canvas, DOWN, 100)


if __name__ == "__main__":
    gui = Gui()
    Thread(target=gui.create).start()
