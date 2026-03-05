"""Release 0.1.0"""

import os
import random
import tkinter as tk
from PIL import ImageGrab
import pytesseract
from deep_translator import GoogleTranslator
import sys
import io

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

ANSWER = []

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>548</width>
    <height>431</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <property name="styleSheet">
   <string notr="true">QMainWindow {
                            background-color: #404040;
                            color: white;
                        }</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QPushButton" name="pushButton">
      <property name="styleSheet">
       <string notr="true">QPushButton {
                            background-color: #008cf0;
                            color: white;
                        }</string>
      </property>
      <property name="text">
       <string>Выбрать область перевода</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QTextEdit" name="textEdit">
      <property name="styleSheet">
       <string notr="true">QTextEdit {
                            background-color: #404040;
                            color: white;
                        }</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(io.StringIO(template), self)

        self.pushButton.clicked.connect(self.check)

    def check(self):
        RegionSelector()
        for i in ANSWER:
            self.textEdit.append(i)
        ANSWER.clear()


def text_from_foto(foto_name):
    a = []
    pytesseract.pytesseract.tesseract_cmd = r'' # укажите верный путь до exe файла tesseract

    text = pytesseract.image_to_string(f'screenshots/{foto_name}.png')
    for i in text.split('\n'):
        if i != "":
            a.append(i.strip())
    translate(a)
    os.remove(f'screenshots/{foto_name}.png')


def translate(text_p):
    global ANSWER
    i = " ".join(text_p)
    # for i in text_p:
    #     ANSWER.append(GoogleTranslator(source='en', target='ru').translate(i))
    ANSWER.append(GoogleTranslator(source='en', target='ru').translate(i))


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
        self.d = random.randint(0, 1000)
        filename = f"screenshots/screenshot_{self.d}.png"

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
        text_from_foto(f"screenshot_{self.d}")
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
