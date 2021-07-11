from PIL import Image
from PIL import ImageGrab
import pyautogui
import time
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


class bb:
    def __init__(self, func):
        self.func = func

    def c(self):
        self.func("aa")


class abb:
    def __init__(self):
        self.bb = bb(self.func)
        self.bb.c()

    def func(self, a):
        print("funciona", a)


d = abb()
