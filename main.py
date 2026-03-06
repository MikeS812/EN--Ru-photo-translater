"""Release 0.1.1"""

import os
import random
import tkinter as tk
from PIL import ImageGrab
import pytesseract
from deep_translator import GoogleTranslator
import sys
import io
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QComboBox, QCheckBox

"""
ANSWER: translated phrase
leng1: the language being translated from
leng2: language for translation
FLAG: the check is necessary to save photos correctly.
"""

ANSWER: list = []
leng1: str = "en"
leng2: str = "ru"
FLAG = False

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>548</width>
    <height>466</height>
   </rect>
  </property>
  <property name="acceptDrops">
   <bool>true</bool>
  </property>
  <property name="windowTitle">
   <string>Экранный переводчик</string>
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
     <widget class="QToolBox" name="toolBox">
      <property name="styleSheet">
       <string notr="true">QToolBox {
    background-color: #404040;
}



QToolBox QWidget {
    background-color: #404040;
    color: white;
}</string>
      </property>
      <property name="currentIndex">
       <number>0</number>
      </property>
      <widget class="QWidget" name="page">
       <property name="geometry">
        <rect>
         <x>0</x>
         <y>0</y>
         <width>530</width>
         <height>394</height>
        </rect>
       </property>
       <attribute name="label">
        <string>Основное окно</string>
       </attribute>
       <layout class="QVBoxLayout" name="verticalLayout_2">
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
         <widget class="QPushButton" name="pushButton_2">
          <property name="styleSheet">
           <string notr="true">QPushButton {
                            background-color: #008cf0;
                            color: white;
                        }</string>
          </property>
          <property name="text">
           <string>Очистить поле</string>
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
      <widget class="QWidget" name="page_2">
       <property name="geometry">
        <rect>
         <x>0</x>
         <y>0</y>
         <width>530</width>
         <height>394</height>
        </rect>
       </property>
       <attribute name="label">
        <string>Настройки</string>
       </attribute>
       <widget class="QCheckBox" name="checkBox">
        <property name="geometry">
         <rect>
          <x>9</x>
          <y>9</y>
          <width>271</width>
          <height>17</height>
         </rect>
        </property>
        <property name="text">
         <string>Сохранять фото</string>
        </property>
       </widget>
       <widget class="QComboBox" name="comboBox_2">
        <property name="geometry">
         <rect>
          <x>221</x>
          <y>33</y>
          <width>59</width>
          <height>18</height>
         </rect>
        </property>
        <item>
         <property name="text">
          <string>ru</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>en</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>de</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>fr</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>es</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>it</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>zh-CN</string>
         </property>
        </item>
        <item>
         <property name="text">
          <string>ja</string>
         </property>
        </item>
       </widget>
       <widget class="QLabel" name="label">
        <property name="geometry">
         <rect>
          <x>89</x>
          <y>33</y>
          <width>126</width>
          <height>16</height>
         </rect>
        </property>
        <property name="text">
         <string>     --------&gt;</string>
        </property>
       </widget>
       <widget class="QComboBox" name="comboBox">
        <property name="geometry">
         <rect>
          <x>10</x>
          <y>33</y>
          <width>59</width>
          <height>18</height>
         </rect>
        </property>
        <item>
         <property name="text">
          <string>en</string>
         </property>
        </item>
       </widget>
      </widget>
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
        self.pushButton_2.clicked.connect(self.clear)
        self.setStyleSheet("""* { font-size: 11pt; }""")
        self.setFixedSize(547, 466)

    def clear(self) -> None:
        self.textEdit.clear()

    def check(self) -> None:
        """
        the function takes the translated text from the photo
        :return: None
        """

        global FLAG
        global leng1
        global leng2

        if self.checkBox.isChecked():
            FLAG = True
        else:
            FLAG = False

        t1 = self.comboBox.currentText()
        t2 = self.comboBox_2.currentText()

        leng1, leng2 = t1, t2

        RegionSelector()
        for i in ANSWER:
            self.textEdit.append(i)
        ANSWER.clear()

        self.textEdit.append("")
        self.textEdit.append("===================================================")
        self.textEdit.append("")


def text_from_foto(foto_name: str) -> None:
    """
    :param foto_name: photo with text
    :return: text with photo
    """

    global FLAG
    a = []
    pytesseract.pytesseract.tesseract_cmd = r''  # укажите верный путь до exe файла tesseract
    
    text = pytesseract.image_to_string(f'screenshots/{foto_name}.png')
    for i in text.split('\n'):
        if i != "":
            a.append(i.strip())

    translate(a)

    if FLAG:
        pass
    else:
        os.remove(f'screenshots/{foto_name}.png')


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
