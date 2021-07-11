# Autoloader
import sys
import os
from pathlib import Path

path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])

# Import system
from search import Search
from errors.screen_errors import ScreenError
import numpy as np
from PIL import Image
from PIL import ImageGrab
import time
import pytesseract
import pyautogui
import win32gui
import colorsys
import threading

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class A:
    def __init__(self):
        print("a")
        self.lala = True
        self.b = "1"
        thread = threading.Thread(target=self.kkkk, args=())
        thread.start()
        time.sleep(2)
        self.b = "2"
        time.sleep(2)
        self.lala = False

    def kkkk(self):
        while self.lala:
            print(self.b)
            time.sleep(1)


print("A")
a = A()
