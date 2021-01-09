from PIL import Image
from PIL import ImageGrab
import pyautogui
import time
import pytesseract

img = Image.open(r'C:\Users\Lucas\Desktop\x\src\sss.png')
print(pytesseract.image_to_string(img,config='--psm 6 --oem 3'))