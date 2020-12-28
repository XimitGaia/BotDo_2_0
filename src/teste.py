import keyboard
import pyautogui
import time
from PIL import Image
from tools.search import Search
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])




class Calculator:

    def __init__(self, radius):
        self.search = Search()
        self.radius = radius
        print(f'Calculating area of circle with radius {self.radius}m')
        self.open_calculator()
        time.sleep(3)
        self.get_pi_position()

    def open_calculator(self):
        pyautogui.moveTo((1,1))
        time.sleep(1)
        pyautogui.click()
        keyboard.write('Calculator')
        time.sleep(0.1)
        keyboard.press_and_release('enter')

    def get_pi_position(self):
        self.image = Image.open(f'{root_path}{os.sep}src{os.sep}pi.png')
        match = self.search.search_image(self.image,match_tolerance=0.1)
        print(match)



calculator = Calculator(10)


