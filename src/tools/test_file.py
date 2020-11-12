import pyautogui
import keyboard
import time
import pytesseract
from PIL import ImageGrab
import re

while True:
    if keyboard.is_pressed("enter"):
        pyautogui.click((297,564))
        time.sleep(0.1)
        pyautogui.press("down")
        time.sleep(0.1)
        pyautogui.click((1050,244))
        time.sleep(0.1)
    if keyboard.is_pressed("."):
        file_name = re.search(r"\d+\.swf",pytesseract.image_to_string(ImageGrab.grab((1092,234,1145,248)), config= '--psm 8 --oem 3 -c tessedit_char_whitelist=.swf0123456789'))[0]
        pyautogui.click((-878,26))
        pyautogui.typewrite(f"{file_name} - ")
        while True:
            if keyboard.is_pressed("enter"):
                pyautogui.press("tab")
                pyautogui.click((800,10))
                break
        # while True:
        #     if keyboard.is_pressed("1"):
        #         pyautogui.typewrite(" - mineral")
        #         pyautogui.click((800,10))
        #         pyautogui.press("enter")
        #         pyautogui.press("tab")
        #         break
        #     elif keyboard.is_pressed("2"):
        #         pyautogui.typewrite(" - peixe")
        #         pyautogui.click((800,10))
        #         pyautogui.press("enter")
        #         pyautogui.press("tab")
        #         break
        #     elif keyboard.is_pressed("3"):
        #         pyautogui.typewrite(" - madeira")
        #         pyautogui.click((800,10))
        #         pyautogui.press("enter")
        #         pyautogui.press("tab")
        #         break
        #     elif keyboard.is_pressed("4"):
        #         pyautogui.typewrite(" - ceral")
        #         pyautogui.click((800,10))
        #         pyautogui.press("enter")
        #         pyautogui.press("tab")
        #         break
        #     elif keyboard.is_pressed("5"):
        #         pyautogui.typewrite(" - personagem")
        #         pyautogui.click((800,10))
        #         pyautogui.press("enter")
        #         pyautogui.press("tab")
        #         break
        #     elif keyboard.is_pressed("6"):
        #         pyautogui.typewrite(" - entrada")
        #         pyautogui.click((800,10))
        #         pyautogui.press("enter")
        #         pyautogui.press("tab")
        #         break
        #     elif keyboard.is_pressed("7"):
        #         pyautogui.typewrite(" - outros")
        #         pyautogui.click((800,10))
        #         pyautogui.press("enter")
        #         pyautogui.press("tab")
        #         break
        #     elif keyboard.is_pressed("esc"):
        #         pyautogui.hotkey("ctrl","z")
        #         pyautogui.click((800,10))
        #         break

        




