from json import loads

from Enemy.Enemy import *


class Gui:
    player: Player
    canvas: Canvas
    win: Tk

    def start_gui(self) -> None:
        self.win = Tk()
        self.win.title("2D Game")
        self.win.attributes('-fullscreen', True)

        self.canvas = Canvas(self.win, height=1080, width=1920, bg="white")
        self.canvas.pack()

        Thread(target=self.start_mission).start()
        # Thread(target=self.start_dev_test).start()

        self.win.mainloop()

    @staticmethod
    def are_all_enemies_dead(enemies: list) -> bool:
        dead_enemies = 0
        for enemy in enemies:
            if enemy.health <= 0:
                dead_enemies += 1

        return dead_enemies == len(enemies)

    def on_player_dead(self) -> None:
        say(self.canvas, text="You lost!", timeout=10)
        self.player.is_game_paused = True
        sleep(10)
        exit()

    def start_dev_test(self) -> None:
        self.player = Player(self.canvas, health=100)

        enemy = Enemy(self.canvas, self.player, 1000, 0, 1)
        enemy.canvas.coords(enemy.enemy, 1920/2, 1080/2)
        enemy.x = 1920/2
        enemy.y = 1080/2
        self.player.enemies.append(enemy)

    def start_mission(self) -> None:
        self.player = Player(self.canvas, health=100)

        waves = loads(open("waves.json", "r").read())
        for wave in waves:
            enemies = []
            self.player.enemies = []

            for i in range(3):
                say(self.canvas, text=wave["name"] + " is coming in " + str(3 - i) + "...", timeout=1)
                sleep(1)

            for i in range(wave["enemy-count"]):
                if self.player.health == 0:
                    self.on_player_dead()

                enemy = Enemy(self.canvas, self.player, wave["enemy"]["health"], wave["enemy"]["damage"], wave["enemy"]["attack-speed"])
                self.player.enemies.append(enemy)
                enemies.append(enemy)
                Thread(target=enemy.auto_move).start()
                sleep(wave["spawn-timeout"])

            while not self.are_all_enemies_dead(enemies):
                if self.player.health == 0:
                    self.on_player_dead()
                sleep(1)

            if self.player.health == 0:
                self.on_player_dead()

        say(self.canvas, text="Congratulations! You won!", timeout=10)
        self.player.is_game_paused = True
        sleep(10)


if __name__ == "__main__":
    gui = Gui()
    gui.start_gui()
