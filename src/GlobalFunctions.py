from tkinter import *
from threading import Thread
from time import sleep

D_UP = 0
D_RIGHT = 1
D_DOWN = 2
D_LEFT = 3


def say(player, canvas: Canvas, text: str = "", timeout: int = 3) -> None:
    text_id = canvas.create_text(1920 / 2, 1080 / 2, font="Normal 40 normal normal", text=text)

    Thread(target=delete_said_text, args=(player, canvas, text_id, timeout)).start()

    return text_id


def alert(canvas: Canvas, text: str = "", timeout: int = 3) -> int:
    text_id = canvas.create_text(1920 / 2, 1080 / 2, font="Normal 40 normal normal", text=text)

    Thread(target=delete_alerted_text, args=(canvas, text_id, timeout)).start()

    return text_id


def delete_alerted_text(canvas: Canvas, text_id: int, timeout: int = 3) -> None:
    if timeout is None:
        return None

    sleep(timeout)

    canvas.delete(text_id)


def delete_said_text(player, canvas: Canvas, text_id: int, timeout: int = 3) -> None:
    while player.is_game_paused:
        sleep(0.2)

    sleep(timeout)

    canvas.delete(text_id)


if __name__ == '__main__':
    pass
