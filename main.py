"""Release 0.1.3"""
import datetime
import os
import tkinter as tk
from PIL import ImageGrab
import pytesseract
from PyQt6.QtCore import pyqtSignal
from deep_translator import GoogleTranslator
import sys
import io
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog

"""
ANSWER: translated phrase
leng1: the language being translated from
leng2: language for translation
FLAG: the check is necessary to save photos correctly.
LOG_FLAG: check to save logs to a txt file
"""

ANSWER: list = []
leng1: str = "en"
leng2: str = "ru"
FLAG = False
LOG_FLAG = True

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
         <layout class="QHBoxLayout" name="horizontalLayout_2">
          <item>
           <widget class="QPushButton" name="pushButton_2">
            <property name="styleSheet">
             <string notr="true">QPushButton {
                            background-color: #008cf0;
                            color: white;
                        }</string>
            </property>
            <property name="text">
             <string>Выбрать текст</string>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QPushButton" name="pushButton_4">
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
           <widget class="QPushButton" name="pushButton_5">
            <property name="styleSheet">
             <string notr="true">QPushButton {
                            background-color: #008cf0;
                            color: white;
                        }</string>
            </property>
            <property name="text">
             <string>Выбрать фото</string>
            </property>
           </widget>
          </item>
         </layout>
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
       <widget class="QCheckBox" name="checkBox_2">
        <property name="geometry">
         <rect>
          <x>10</x>
          <y>70</y>
          <width>171</width>
          <height>17</height>
         </rect>
        </property>
        <property name="text">
         <string>Сохранять историю</string>
        </property>
       </widget>
       <widget class="QPushButton" name="pushButton_3">
        <property name="geometry">
         <rect>
          <x>10</x>
          <y>100</y>
          <width>141</width>
          <height>23</height>
         </rect>
        </property>
        <property name="text">
         <string>Загрузить историю</string>
        </property>
       </widget>
       <widget class="QPushButton" name="pushButton_6">
        <property name="geometry">
         <rect>
          <x>10</x>
          <y>130</y>
          <width>141</width>
          <height>23</height>
         </rect>
        </property>
        <property name="text">
         <string>Очистить историю</string>
        </property>
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

text_menu = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>menu</class>
 <widget class="QWidget" name="menu">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>322</width>
    <height>200</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <property name="styleSheet">
   <string notr="true">QWidget {
                            background-color: #404040;
                            color: white;
                        }</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout_2">
     <item>
      <widget class="QComboBox" name="comboBox_4">
       <item>
        <property name="text">
         <string>en</string>
        </property>
       </item>
       <item>
        <property name="text">
         <string>ru</string>
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
     </item>
     <item>
      <widget class="QLabel" name="label">
       <property name="text">
        <string>              -&gt;</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QComboBox" name="comboBox_3">
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
     </item>
    </layout>
   </item>
   <item>
    <widget class="QTextEdit" name="textEdit"/>
   </item>
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout">
     <item>
      <widget class="QPushButton" name="pushButton">
       <property name="text">
        <string>Перевести</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="pushButton_2">
       <property name="text">
        <string>Отмена</string>
       </property>
      </widget>
     </item>
    </layout>
   </item>
  </layout>
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
        self.pushButton_4.clicked.connect(self.clear)
        self.pushButton_3.clicked.connect(self.open_log)
        self.pushButton_2.clicked.connect(self.translator)
        self.pushButton_5.clicked.connect(self.photo_perevod)
        self.pushButton_6.clicked.connect(self.delete_log)

        self.translator_window = None

        self.setStyleSheet("""* { font-size: 10.5pt; }""")

        self.setFixedSize(547, 466)
        os.makedirs("screenshots", exist_ok=True)
        if "log.txt" in os.listdir("screenshots"):
            pass
        else:
            with open("screenshots/log.txt", 'w', encoding='utf-8') as f:
                f.write(f'{datetime.datetime.now()}')

    def delete_log(self):
        with open("screenshots/log.txt", "w") as f:
            pass

    def translator(self):
        self.translator_window = Translator()
        self.translator_window.translation.connect(self.on_t)
        self.translator_window.show()

    def on_t(self, translated_text):
        self.textEdit.append("")
        self.textEdit.append(f"Текстовый перевод: {translated_text}")
        self.textEdit.append("")

    def photo_perevod(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Открыть фото", "", "All files (*)"
        )
        if not path:
            return

        text_from_foto(path, 1)
        if LOG_FLAG:
            f = open("screenshots/log.txt", "a", encoding='utf-8')

        t1 = self.comboBox.currentText()
        t2 = self.comboBox_2.currentText()

        leng1, leng2 = t1, t2


        for i in ANSWER:
            self.textEdit.append(i)
            if LOG_FLAG:
                print(i, file=f)
        ANSWER.clear()

        self.textEdit.append("")
        self.textEdit.append("==================================================")
        self.textEdit.append("")

    def clear(self) -> None:
        self.textEdit.clear()

    def open_log(self):
        with open("screenshots/log.txt", "r", encoding='utf-8') as log_file:
            data1 = log_file.readlines()

        if len(data1) != 0:
            for i in data1:
                self.textEdit.append(i)

        self.textEdit.append("")
        self.textEdit.append("==================================================")
        self.textEdit.append("")

    def check(self) -> None:
        """
        the function takes the translated text from the photo
        :return: None
        """

        global FLAG, leng1, leng2, LOG_FLAG

        FLAG = self.checkBox.isChecked()
        LOG_FLAG = self.checkBox_2.isChecked()

        if LOG_FLAG:
            f = open("screenshots/log.txt", "a", encoding='utf-8')

        t1 = self.comboBox.currentText()
        t2 = self.comboBox_2.currentText()

        leng1, leng2 = t1, t2

        RegionSelector()
        for i in ANSWER:
            self.textEdit.append(i)
            if LOG_FLAG:
                print(i, file=f)
        ANSWER.clear()

        self.textEdit.append("")
        self.textEdit.append("==================================================")
        self.textEdit.append("")


class Translator(QWidget):
    translation = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi(io.StringIO(text_menu), self)
        self.pushButton_2.clicked.connect(self.off_f)
        self.pushButton.clicked.connect(self.translate_text)

        self.setFixedSize(322, 200)

    def off_f(self):
        self.close()

    def translate_text(self):
        text = self.textEdit.toPlainText()
        l1, l2 = self.comboBox_4.currentText(), self.comboBox_3.currentText()
        self.translation.emit(GoogleTranslator(source=l1, target=l2).translate(text))


def text_from_foto(foto_name: str, flag: int) -> None:
    """
    :param flag: flag func
    :param foto_name: photo with text
    :return: text with photo
    """

    global FLAG
    a = []
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Admin\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'  # укажите верный путь до exe файла tesseract

    if flag == 0:
        text = pytesseract.image_to_string(f'screenshots/{foto_name}')
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
