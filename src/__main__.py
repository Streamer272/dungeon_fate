from typing import List
from os import listdir

from src.Enemy.Enemy import *
from src.Player.Player import *
from src.Player.Weapons.Weapon import *


class Gui:
    """
    gui controller
    """

    def start_gui(self) -> None:
        """
        creates basic gui
        """

        self.win = Tk()
        self.win.title("2D Game")
        self.win.attributes('-fullscreen', True)

        self.canvas = Canvas(self.win, height=1080, width=1920, bg="white")
        self.canvas.pack()

        self.create_menu()

        self.win.focus_force()
        self.win.mainloop()

    def create_menu(self):
        """
        creates game menu
        """

        self.exit_button = Button(self.win, text="Exit", font=("Normal", 15, "normal"), command=self.exit_game)
        self.exit_button.place(x=15, y=15)
        self.start_button = Button(self.win, text="Start", font=("Normal", 30, "normal"),
                                   command=self.start_game)
        self.start_button.place(x=1920 / 2 - 45, y=1080 / 2 + 150)

        self.mode_label = Label(self.win, text="Game mode: ")
        self.mode_label.place(x=1920 / 2 - 100, y=1080 / 2 + 5)
        self.mode = StringVar(self.win)
        self.mode.set("Practise")
        mode_options = ["Practise", "Dev Test", "Multiplayer"]
        self.mode_menu = OptionMenu(self.win, self.mode, *mode_options)
        self.mode_menu.place(x=1920 / 2 - 20, y=1080 / 2)

        self.operator_label = Label(self.win, text="Operators: ")
        self.operator_label.place(x=1920 / 2 - 85, y=1080 / 2 + 5 + 50)
        self.operator = StringVar(self.win)
        self.operator.set("Ninja")
        classes_options = listdir("src/Player/Operators")
        self.operator_option_menu = OptionMenu(self.win, self.operator, *classes_options)
        self.operator_option_menu.place(x=1920 / 2 - 20, y=1080 / 2 + 50)

        self.resource_pack_label = Label(self.win, text="Resource pack: ")
        self.resource_pack_label.place(x=1920 / 2 - 110, y=1080 / 2 + 5 + 100)
        self.resource_pack = StringVar(self.win)
        self.resource_pack.set("normal")
        resource_pack_options = listdir("resource-packs")
        self.resource_pack_option_menu = OptionMenu(self.win, self.resource_pack, *resource_pack_options)
        self.resource_pack_option_menu.place(x=1920 / 2 - 20, y=1080 / 2 + 100)

    def delete_menu(self):
        """
        deletes game menu
        """

        self.exit_button.place_forget()
        self.start_button.place_forget()
        self.mode_label.place_forget()
        self.mode_menu.place_forget()
        self.resource_pack_label.place_forget()
        self.resource_pack_option_menu.place_forget()
        self.operator_label.place_forget()
        self.operator_option_menu.place_forget()

    def exit_game(self):
        """
        forcibly exites game
        """

        self.win.destroy()
        exit()

    def start_game(self) -> None:
        """
        starts game
        :return: Nonetype
        """

        self.delete_menu()

        if self.mode.get() == "Practise":
            Thread(target=self.start_practise).start()

        elif self.mode.get() == "Dev Text":
            Thread(target=self.start_dev_test).start()

        elif self.mode.get() == "Multiplayer":
            acc_cont = AccountController()
            Thread(target=acc_cont.ask_for_login).start()
            acc_cont.wait_until_done()
            if acc_cont.is_server_offline:
                error_text_id = alert(self.canvas, text="Sorry, the server is offline", timeout=None)
                return None

            Thread(target=self.start_multiplayer).start()

    def start_multiplayer(self) -> None:
        """
        starts multiplayer game
        """

        self.player = Player(self)

    def start_practise(self) -> None:
        """
        starts practice game
        :return: Nonetype
        """

        self.player = Player(self)

        def are_all_enemies_dead(enemies_: List[Enemy]) -> bool:
            """
            returns true if all enemies are dead
            :param enemies_:
            :return: bool
            """

            dead_enemies = 0
            for enemy_ in enemies_:
                if enemy_.health <= 0:
                    dead_enemies += 1

            return dead_enemies == len(enemies_)

        waves = loads(open("src/Data/Levels/practise.json", "r").read())
        for wave in waves:
            enemies = []
            self.player.enemies = []

            for i in range(3):
                say(self.player, self.canvas, text=wave["name"] + " is coming in " + str(3 - i) + "...", timeout=1)
                sleep(1)

                while self.player.is_game_paused:
                    sleep(0.2)

            for i in range(wave["enemy-count"]):
                if self.player.health == 0:
                    self.on_player_dead()

                while self.player.is_game_paused:
                    sleep(0.2)

                enemy = Enemy(self.player, wave["enemy"]["health"], wave["enemy"]["damage"],
                              wave["enemy"]["attack-speed"])
                self.player.enemies.append(enemy)
                enemies.append(enemy)
                Thread(target=enemy.auto_move).start()
                sleep(wave["spawn-timeout"])

            while not are_all_enemies_dead(enemies):
                if self.player.health == 0:
                    self.on_player_dead()
                sleep(1)

            if self.player.health == 0:
                self.on_player_dead()

        say(self.player, self.canvas, text="Congratulations! You won!", timeout=10)
        self.player.is_game_paused = True
        sleep(10)

    def start_dev_test(self) -> None:
        """
        starts developer test
        """

        self.player = Player(self)

        enemy = Enemy(self.canvas, self.player, 1000, 0, 1)
        enemy.canvas.coords(enemy.enemy, 1920/2, 1080/2)
        enemy.x = 1920/2
        enemy.y = 1080/2
        self.player.enemies.append(enemy)

    def on_player_dead(self) -> None:
        """
        on player dead
        """

        say(self.player, self.canvas, text="You lost!", timeout=10)
        sleep(10)
        self.exit_game()


if __name__ == "__main__":
    gui = Gui()
    gui.start_gui()
