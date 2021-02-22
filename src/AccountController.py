from threading import Thread
from tkinter import *
from json import loads, dumps
from os import path
from threading import Thread
from time import sleep
from tkinter import Label, Entry, Button

import requests


class AccountController:
    license_entry: Entry
    license_label: Label
    login_button: Button
    register_button: Button
    name_entry: Entry
    password_entry: Entry
    password_label: Label
    label: Label
    name_label: Label
    win: Tk
    return_value: bool

    def __init__(self):
        self.backend_url = "http://localhost:8012/"

    @staticmethod
    def is_user_logged_in() -> bool:
        return path.exists("Data/User_Data/data.json")

    def send_login_request(self, username: str, password: str) -> requests.request:
        data = {
            "username": username,
            "password": password
        }

        response = requests.post(self.backend_url + "login/", json=data)

        return response

    def send_register_request(self, username: str, password: str, license_key: str) -> requests.request:
        data = {
            "username": username,
            "password": password,
            "license_key": license_key
        }

        response = requests.post(self.backend_url + "register/", json=data)

        return response

    def login(self, name: str, password: str) -> None:
        response = self.send_login_request(name, password)

        if response.status_code == 200:
            self.label.config(text="Login successful")
            self.return_value = True
            sleep(1)
            self.win.destroy()

        elif response.status_code == 401:
            self.label.config(text="Wrong username, check your spelling and try again")

        elif response.status_code == 402:
            self.label.config(text="Wrong password, check your spelling and try again")

    def register(self, username: str, password: str, license_key: str):
        response = self.send_register_request(username, password, license_key)

        if response.status_code == 200:
            self.label.config(text="Register successful")
            self.return_value = True
            sleep(1)
            self.win.destroy()

        elif response.status_code == 401:
            label.config(text="User with that username already exists")

        elif response.status_code == 403:
            label.config(text="License key isn't valid")

    def submit_login(self) -> None:
        username = self.name_entry.get()
        password = self.password_entry.get()

        if username == "":
            self.label.config(text="Please enter your full username")
        elif password == "":
            self.label.config(text="Please enter your full password")
        else:
            self.label.config(text="Processing login... Please wait...")
            Thread(target=self.login, args=[username, password]).start()

    def submit_register(self) -> None:
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
            Thread(target=self.register, args=[username, password, license_key]).start()

    def create_register_win(self) -> None:
        self.win.geometry("200x130")
        self.register_button.place_forget()

        self.license_label = Label(self.win, text="License key: ")
        self.license_label.place(x=0, y=75)
        self.license_entry = Entry(self.win)
        self.license_entry.place(x=70, y=77)

        self.login_button.config(text="Register", command=lambda: Thread(target=self.submit_register).start())
        self.login_button.place(x=142, y=100)

    def ask_for_login(self) -> bool:
        self.win = Tk()
        self.win.title("Login")
        self.win.geometry("200x125")
        self.win.resizable(0, 0)

        self.return_value: bool = False

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

        self.login_button = Button(self.win, text="Login", command=lambda: Thread(target=self.submit_login).start())
        self.login_button.place(x=152, y=80)

        self.register_button = Button(self.win, text="No account?\nCreate one",
                                      command=lambda: Thread(target=self.create_register_win).start())
        self.register_button.place(x=10, y=80)

        self.name_entry.focus_force()
        self.win.focus_force()
        self.win.mainloop()

        return self.return_value


if __name__ == '__main__':
    pass
