from json import loads
from tkinter import StringVar, OptionMenu, Button, Label
from typing import List
from tkinter import *
from os import listdir

from Enemy.Enemy import *


class Gui:
    operator_label: Label
    operator: StringVar
    operator_option_menu: OptionMenu
    resource_pack_label: Label
    exit_button: Button
    resource_pack_option_menu: OptionMenu
    resource_pack: StringVar
    start_button: object
    pistol: object
    player: Player
    canvas: Canvas
    win: Tk

    def start_gui(self) -> None:
        self.win = Tk()
        self.win.title("2D Game")
        self.win.attributes('-fullscreen', True)

        self.canvas = Canvas(self.win, height=1080, width=1920, bg="white")
        self.canvas.pack()

        self.exit_button = Button(self.win, text="Exit", font=("Normal", 15, "normal"), command=self.exit_game)
        self.exit_button.place(x=15, y=15)

        self.create_menu()

        self.win.focus_force()
        self.win.mainloop()

    def create_menu(self):
        self.start_button = Button(self.win, text="Start", font=("Normal", 30, "normal"), command=self.start_game)
        self.start_button.place(x=1920 / 2 - 45, y=1080 / 2 + 150)

        self.resource_pack_label = Label(self.win, text="Resource pack: ")
        self.resource_pack_label.place(x=1920 / 2 - 110, y=1080 / 2 + 5 + 100)
        self.resource_pack = StringVar(self.win)
        self.resource_pack.set("normal")
        resource_pack_options = listdir("resource-packs")
        self.resource_pack_option_menu = OptionMenu(self.win, self.resource_pack, *resource_pack_options)
        self.resource_pack_option_menu.place(x=1920 / 2 - 20, y=1080 / 2 + 100)

        self.operator_label = Label(self.win, text="Operators: ")
        self.operator_label.place(x=1920 / 2 - 85, y=1080 / 2 + 5 + 50)
        self.operator = StringVar(self.win)
        self.operator.set("Ninja")
        classes_options = listdir("Player/Operators")
        self.operator_option_menu = OptionMenu(self.win, self.operator, *classes_options)
        self.operator_option_menu.place(x=1920 / 2 - 20, y=1080 / 2 + 50)

    def start_game(self):
        self.start_button.place_forget()
        self.resource_pack_label.place_forget()
        self.resource_pack_option_menu.place_forget()
        self.operator_label.place_forget()
        self.operator_option_menu.place_forget()
        Thread(target=self.start_mission).start()
        # Thread(target=self.start_dev_test).start()

    def exit_game(self):
        self.win.destroy()
        exit()

    @staticmethod
    def are_all_enemies_dead(enemies: List[Enemy]) -> bool:
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
        self.player = Player(self.canvas, self.resource_pack.get(), self.operator.get(), health=100)
        # enemy = Enemy(self.canvas, self.player, 1000, 0, 1)
        # enemy.canvas.coords(enemy.enemy, 1920/2, 1080/2)
        # enemy.x = 1920/2
        # enemy.y = 1080/2
        # self.player.enemies.append(enemy)
        self.pistol = Weapon(self.player, "Pistol1")
        sleep(1)
        Thread(target=self.run_bullet_test()).start()

    def run_bullet_test(self):
        print("Running bullet test")
        self.pistol.shoot_bullet()

    def start_mission(self) -> None:
        self.player = Player(self.canvas, self.resource_pack.get(), self.operator.get(), health=100)

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

                enemy = Enemy(self.player, wave["enemy"]["health"], wave["enemy"]["damage"], wave["enemy"]["attack-speed"])
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
