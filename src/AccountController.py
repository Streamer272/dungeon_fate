from threading import Thread
from tkinter import *
from json import loads, dumps
from os import path
from threading import Thread
from time import sleep

import requests


class AccountController:
    win: Tk
    return_value: bool

    def __init__(self):
        self.backend_url = "http://localhost:8012/"

    @staticmethod
    def is_user_logged_in() -> bool:
        return path.exists("Data/User_Data/data.json")

    def start_login_request(self, username: str, password: str) -> requests.request:
        data = {
            "username": username,
            "password": password
        }

        response = requests.post(self.backend_url + "login/", json=data)

        print("Status code: " + str(response.status_code) + "\nText: " + str(response.text))
        return response

    def login(self, label: Label, name: str, password: str) -> None:
        print("Got to login")
        response = self.start_login_request(name, password)

        if response.status_code == 200:
            label.config(text="Login successful")
            self.return_value = True
            sleep(1)
            self.win.destroy()

        elif response.status_code == 401:
            label.config(text="Wrong username, check your spelling and try again")

        elif response.status_code == 402:
            label.config(text="Wrong password, check your spelling and try again")

    def ask_for_login(self) -> bool:
        self.win = Tk()
        self.win.title("Login")
        self.win.geometry("200x110")
        self.win.resizable(0, 0)

        self.return_value: bool = False

        label = Label(self.win, text="To enter the game you need to log in", wraplength=200)
        label.place(x=100, y=20, anchor="center")

        name_label = Label(self.win, text="Username: ")
        name_label.place(x=5, y=35)
        name_entry = Entry(self.win)
        name_entry.place(x=65, y=37)

        password_label = Label(self.win, text="Password: ")
        password_label.place(x=5, y=55)
        password_entry = Entry(self.win, show="*")
        password_entry.place(x=65, y=57)

        def submit(self_, e: any = None) -> None:
            del e

            print("Got to submit")
            name = name_entry.get()
            password = password_entry.get()

            if name == "":
                label.config(text="Please enter your full name")
            elif password == "":
                label.config(text="Please enter your full password")
            else:
                label.config(text="Processing login... Please wait...")
                Thread(target=self_.login, args=[label, name, password]).start()

        login_button = Button(self.win, text="Login", command=lambda: Thread(target=submit, args=[self]).start())
        login_button.place(x=148, y=80)

        name_entry.focus_force()
        password_entry.bind("<Return>", lambda e: Thread(target=submit, args=[self, e]).start())
        self.win.focus_force()
        self.win.mainloop()

        return self.return_value


if __name__ == '__main__':
    pass
