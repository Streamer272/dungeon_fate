"""
account controller file
"""

from threading import Thread
from tkinter import *
from json import loads, dumps
from os import path
from threading import Thread
from time import sleep
from tkinter import Label, Entry, Button

import requests


class AccountController:
    """
    account controller for multiplayer
    """

    def __init__(self):
        self.backend_url = "http://localhost:8012/"
        self.is_server_offline = False
        self.logged_in = False

    def __is_user_logged_in(self) -> bool:
        """
        returns bool is user if logged in
        :return: bool
        """

        if path.exists("Data/User_Data/data.json"):
            data = loads(open("Data/User_Data/data.json", "r").read())

            self.__login(data["username"], data["password"])

        return False

    @staticmethod
    def __write_data(username: str, password: str) -> None:
        """
        writes data to cookie
        :param username:
        :param password:
        """

        with open("Data/User_Data/data.json", "w") as file:
            file.write(dumps({
                "logged_in": True,
                "data": {
                    "username": username,
                    "password": password,
                }
            }))
            file.close()

    def __send_login_request(self, username: str, password: str) -> requests.request:
        """
        sends login request to server
        :param username:
        :param password:
        :return:
        """

        data = {
            "username": username,
            "password": password
        }

        response = requests.post(self.backend_url + "login/", json=data)

        return response

    def __send_register_request(self, username: str, password: str, license_key: str) -> requests.request:
        """
        sends register request to server
        :param username:
        :param password:
        :param license_key:
        :return:
        """

        data = {
            "username": username,
            "password": password,
            "license_key": license_key
        }

        response = requests.post(self.backend_url + "register/", json=data)

        return response

    def __login(self, username: str, password: str) -> None:
        """
        logs in
        :param username:
        :param password:
        :return:
        """

        try:
            response = self.__send_login_request(username, password)

        except:
            self.is_server_offline = True
            self.win.destroy()
            return None

        if response.status_code == 200:
            self.__write_data(username, password)

            self.label.config(text="Login successful")
            self.logged_in = True
            sleep(1)
            self.win.destroy()

        elif response.status_code == 401:
            self.label.config(text="Wrong username, check your spelling and try again")

        elif response.status_code == 402:
            self.label.config(text="Wrong password, check your spelling and try again")

    def __register(self, username: str, password: str, license_key: str):
        """
        registers
        :param username:
        :param password:
        :param license_key:
        :return:
        """

        try:
            response = self.__send_register_request(username, password, license_key)

        except:
            self.is_server_offline = True
            self.win.destroy()
            return None

        if response.status_code == 200:
            self.__write_data(username, password)

            self.label.config(text="Register successful")
            self.logged_in = True
            sleep(1)
            self.win.destroy()

        elif response.status_code == 401:
            self.label.config(text="User with that username already exists")

        elif response.status_code == 403:
            self.label.config(text="License key isn't valid")

    def __submit_login(self) -> None:
        """
        on login button click
        """

        username = self.name_entry.get()
        password = self.password_entry.get()

        if username == "":
            self.label.config(text="Please enter your full username")
        elif password == "":
            self.label.config(text="Please enter your full password")
        else:
            self.label.config(text="Processing login... Please wait...")
            Thread(target=self.__login, args=[username, password]).start()

    def __submit_register(self) -> None:
        """
        on register button click
        """

        username = self.name_entry.get()
        password = self.password_entry.get()
        license_key = self.license_entry.get()

        if len(username) < 5:
            self.label.config(text="Username must have at least 5 characters")
        elif " " in username:
            self.label.config(text="Username can't have spaces")

        elif len(password) < 6:
            self.label.config(text="Password must have at least 6 characters")
        elif " " in password:
            self.label.config(text="Password can't have spaces")

        elif len(license_key) != 11 or "-" not in license_key:
            self.label.config(text="License key format is not valid")

        else:
            self.label.config(text="Processing register... Please wait...")
            Thread(target=self.__register, args=[username, password, license_key]).start()

    def __create_register_win(self) -> None:
        """
        creates register window
        """

        self.win.geometry("200x130")
        self.register_button.place_forget()

        self.license_label = Label(self.win, text="License key: ")
        self.license_label.place(x=0, y=75)
        self.license_entry = Entry(self.win)
        self.license_entry.place(x=70, y=77)

        self.login_button.config(text="Register", command=lambda: Thread(target=self.__submit_register).start())
        self.login_button.place(x=142, y=100)

    def __on_delete_window(self) -> None:
        """
        on delete window
        """

        if self.logged_in or self.is_server_offline:
            self.win.destroy()

    def wait_until_done(self) -> None:
        """
        waits until login is done
        """

        while not self.logged_in and not self.is_server_offline:
            sleep(0.5)
        sleep(1)

    def ask_for_login(self) -> bool:
        """
        creates main win
        :return:
        """

        if self.__is_user_logged_in():
            return True

        self.win = Tk()
        self.win.title("Login")
        self.win.geometry("200x125")
        self.win.resizable(0, 0)
        self.win.protocol("WM_DELETE_WINDOW", self.__on_delete_window)

        self.label = Label(self.win, text="To enter the game you need to log in", wraplength=200)
        self.label.place(x=100, y=20, anchor="center")

        self.name_label = Label(self.win, text="Username: ")
        self.name_label.place(x=5, y=35)
        self.name_entry = Entry(self.win)
        self.name_entry.place(x=70, y=37)

        self.password_label = Label(self.win, text="Password: ")
        self.password_label.place(x=5, y=55)
        self.password_entry = Entry(self.win, show="*")
        self.password_entry.place(x=70, y=57)

        self.login_button = Button(self.win, text="Login", command=lambda: Thread(target=self.__submit_login).start())
        self.login_button.place(x=152, y=80)

        self.register_button = Button(self.win, text="No account?\nCreate one",
                                      command=lambda: Thread(target=self.__create_register_win).start())
        self.register_button.place(x=10, y=80)

        self.name_entry.focus_force()
        self.win.focus_force()
        self.win.mainloop()


if __name__ == '__main__':
    pass
