import argparse
import datetime
import json
import os
import time
import tkinter as tk
from PIL import ImageGrab
import pytesseract
from deep_translator import GoogleTranslator
from PyQt6 import uic


if not os.path.exists('screenshots'):
    os.makedirs('screenshots')


if not os.path.exists('screenshots/pt.txt'):
    with open('screenshots/pt.txt', 'w', encoding='utf-8') as f:
        f.write('')

"""
ANSWER: translated phrase
leng1: the language being translated from
leng2: language for translation
FLAG: the check is necessary to save photos correctly.
LOG_FLAG: check to save logs to a txt file
"""
r"""C:\Users\Admin\PycharmProjects\EN--Ru-photo-translaterам\console_translator.py"""

ANSWER: list = []
leng1: str = "en"
leng2: str = "ru"
FLAG: bool = False
LOG_FLAG: bool = True

PATH: str = open("screenshots/pt.txt").readline().strip()

parser = argparse.ArgumentParser()
parser.add_argument("-trl", action='store_true', help="При запуске с этим ключом будет доступен выбор области перевода")
parser.add_argument("-pth", type=str, help="Путь до файла tesseract")
args = parser.parse_args()

def set_path():
    global PATH
    if args.pth:
        print(args.pth, file=open("screenshots/pt.txt", "w"))
        print("Путь установлен")

def text_from_foto(foto_name: str, flag: int) -> None:
    """
    :param flag: flag func
    :param foto_name: photo with text
    :return: text with photo
    """

    global FLAG
    a = []

    pytesseract.pytesseract.tesseract_cmd = PATH

    if flag == 0:
        try:
            text = pytesseract.image_to_string(f'screenshots/{foto_name}')
        except Exception as e:
            jsn = {"Error": str(e), "data": str(datetime.datetime.now()), "part_of_the_code": "text_from_foto"}
            with open('screenshots/log_error.json', 'w', encoding="utf-8") as f:
                json.dump(jsn, f, indent=4, sort_keys=True)
            text = "error, check the path to the tesseract file"
        for i in text.split('\n'):
            if i != "":
                a.append(i.strip())

        translate(a)

        if FLAG:
            pass
        else:
            os.remove(f'screenshots/{foto_name}')
    elif flag == 1:
        text = pytesseract.image_to_string(foto_name)
        for i in text.split('\n'):
            if i != "":
                a.append(i.strip())

        translate(a)



def translate(text_p: list[str]) -> None:
    """
    :param text_p: the text to be translated
    :return: translated text
    """

    global ANSWER
    i = " ".join(text_p)
    ANSWER.append(GoogleTranslator(source=leng1, target=leng2).translate(i))


class RegionSelector:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.1)
        self.root.configure(bg='gray')

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.region = None

        self.canvas = tk.Canvas(self.root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.root.mainloop()

    def s(self):
        self.fil = "".join(f"screenshot_{str(datetime.datetime.now())}.png".split()).replace(':', '-')
        filename = f"screenshots/{self.fil}"

        screenshot = ImageGrab.grab(bbox=self.region)
        screenshot.save(filename)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline='red', width=2
        )

    def on_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        self.region = (x1, y1, x2, y2)
        self.s()
        text_from_foto(self.fil, 0)
        self.root.quit()
        self.root.destroy()


def start_trl() -> None | str:
    RegionSelector()

    """ This is text, and i want translate it """
    """ This is text number two, and i want translate it """

    time.sleep(1)

    if ANSWER:
        print(*ANSWER)

if args.trl:
    start_trl()

if args.pth:
    set_path()