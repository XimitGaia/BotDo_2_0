import pyautogui
from PIL import ImageGrab
import PIL
from PIL import Image
import time
import pytesseract
import cv2
from pytesseract import Output
import numpy as np

screen_size = ImageGrab.grab('').size
region_to_search = (screen_size[0] * 0.20863836017, screen_size[1] * 0.39322916667,screen_size[0] * 0.4450951683748,screen_size[1] * 0.825520833333334)
pyautogui.moveTo((region_to_search[0],region_to_search[1]))
pyautogui.moveTo((region_to_search[2],region_to_search[3]))
# a = (286,302,609,634)
# img = ImageGrab.grab(region_to_search)
# #img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
# data = pytesseract.image_to_data(img, output_type=Output.DICT, config ='--psm 6 --oem 3')
# i = data['text'].index('Pepinous')

# x, y, w, h = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
# pyautogui.moveTo(286+x +w/2 ,302+y +h/2)