from threading import Thread
from tkinter import *
from json import loads, dumps
from os import path


class AccountController:
    def __init__(self):
        pass

    @staticmethod
    def is_user_logged_in() -> None:
        return path.exists("Data/Account_Data/data.json")

    @staticmethod
    def ask_login() -> None:
        win = Tk()
        win.title("Login")
        win.geometry("200x85")
        win.resizable(0, 0)

        email_label = Label(win, text="Email: ")
        email_label.place(x=15, y=10)
        email_entry = Entry(win)
        email_entry.place(x=65, y=12)

        password_label = Label(win, text="Password: ")
        password_label.place(x=5, y=30)
        password_entry = Entry(win, show="*")
        password_entry.place(x=65, y=32)

        login_button = Button(win, text="Login")
        login_button.place(x=95, y=55)

        register_button = Button(win, text="Register")
        register_button.place(x=137, y=55)

        win.mainloop()


if __name__ == '__main__':
    pass
