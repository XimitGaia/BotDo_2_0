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


#proportioon Widht_screen/width_action_screen = 1.415
#proportion width_sction_screen/high_action_scrren = 1.255

image = Image.open(r"C:\Users\Lucas\Desktop\aaaa.png")
image = image.convert(mode='HSV')
pixel = image.load()
count = 110
v_o  = 178
s_o = 46
s_f = 255
v_f = 255
for j in range(4):
    v = int(v_f - j*(77//4))
    #v = int(v_o + j*(77//4))
    for i in range(4):
        step_s = 1
        #s = int(s_f - i*(46//4))
        s = int(s_o + i*(209//4))
        r = int((v/s)*6)
        start = 131 - r
        end = 131 + r
        h_o = 63
        h_f = 191
        first = True
        ends = True
        for a in range(image.size[1]):
            h = int(h_o + a*(h_f - h_o)/image.size[1])
            print(h)
            if first and h > start:
                h = 0
                first = False
            if ends and h > end:
                h = 0
                ends = False
            for b in range(image.size[0]):
                pixel[b,a] = (h, s, v)
        image.show()

    count += 1


# b = [0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.010050251256281407, 0.02512562814070352]
# a = []
# media = sum(a)/len(a)
# k = 0.10050251256281408
# desv_pad = (0.010050251256281407 - media)**2
# print(f'media {sum(a)/len(a)}, desv {desv_pad}')












# e = []
# c = []
# last_group = None
# for key, value in row_dict.items():
#     print(key)
#     if value < 0.011:
#         e.append(key)

#     else:
#         c.append(key)

# print('e',e,'c',c)