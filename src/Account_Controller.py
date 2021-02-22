from threading import Thread
from tkinter import *
from json import loads, dumps
from os import path
from requests import post, get, put, request


class AccountController:
    def __init__(self):
        pass

    @staticmethod
    def is_user_logged_in() -> bool:
        return path.exists("Data/User_Data/data.json")

    @staticmethod
    def ask_login() -> None:
        win = Tk()
        win.title("Login")
        win.geometry("200x110")
        win.resizable(0, 0)

        label = Label(win, text="Enter your username and password please:", wraplength=200)
        label.place(x=100, y=20, anchor="center")

        name_label = Label(win, text="Username: ")
        name_label.place(x=5, y=35)
        name_entry = Entry(win)
        name_entry.place(x=65, y=37)

        password_label = Label(win, text="Password: ")
        password_label.place(x=5, y=55)
        password_entry = Entry(win, show="*")
        password_entry.place(x=65, y=57)

        def login():
            name = name_entry.get()
            password = password_entry.get()

            if name == "":
                label.config(text="Username can't be empty, please enter your full username")
            elif password == "":
                label.config(text="Password can't be empty, please enter your full password")
            else:
                label.config(text="Processing login... Please wait...")

        login_button = Button(win, text="Login", command=login)
        login_button.place(x=148, y=80)

        win.mainloop()


if __name__ == '__main__':
    pass
