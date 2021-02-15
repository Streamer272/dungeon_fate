from tkinter import *
from threading import Thread
from time import sleep

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3


def say(canvas: Canvas, text: str = "", timeout: int = 3):
    text_id = canvas.create_text(1920/2, 1080/2, font="Normal 40 normal normal", text=text)
    Thread(target=delete_text, args=(canvas, text_id, timeout)).start()


def delete_text(canvas: Canvas, text_id: int, timeout: int = 3):
    sleep(timeout)
    canvas.delete(text_id)


if __name__ == '__main__':
    pass
