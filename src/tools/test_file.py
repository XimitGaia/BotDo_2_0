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


#proportioon Widht_screen/width_action_screen = 1.415
#proportion width_sction_screen/high_action_scrren = 1.255

row_dict = dict()
image = ImageGrab.grab((6,4,200,55))
hsv = image.convert('HSV')
matrix = np.array(image)

line_number = 0
for line in matrix:
    bright_pixels = 0
    for item in line:
        if item[0] > 200 and item[1] > 200 and item[2] > 200:
            bright_pixels += 1
    density = bright_pixels/len(line)
    row_dict.update({(line_number): density})
    line_number += 1
print(row_dict.values())

# b = [0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.02512562814070352]
# a = []
# media = sum(a)/len(a)
# k = 0.10050251256281408
# desv_pad = (0.010050251256281407 - media)**2
# print(f'media {sum(a)/len(a)}, desv {desv_pad}')












e = []
c = []
last_group = None
for key, value in row_dict.items():
    print(key)
    if value < 0.011:
        e.append(key)

    else:
        c.append(key)

print('e',e,'c',c)