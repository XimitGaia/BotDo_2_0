import pytesseract
import pyautogui
import keyboard
import time
from PIL import Image
from PIL import ImageGrab
import re
from sqlite import Database
import os




def get_barrers():
    x_signal = input('X signal: ')
    y_signal = input('Y signal: ')
    barrers = []
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Selection is on')
    while True:
        if keyboard.is_pressed('space'):
            mouse_pos = pyautogui.position()
            area = (mouse_pos[0]+5 , mouse_pos[1] + 10 ,mouse_pos[0]+63 ,mouse_pos[1]+24)
            foto = ImageGrab.grab(area)
            pos = re.findall(r'(\d+)',pytesseract.image_to_string(foto,config='--psm 13 --oem 3 -c tessedit_char_whitelist=,0123456789'))
            if x_signal == '-':
                pos[0] = '-' + pos[0]
            if y_signal == '-':
                pos[1] = '-' + pos[1]
            cell = [int(pos[0]),int(pos[1]),0,0,0,0]
            while True:
                if keyboard.is_pressed('w'):
                    cell[2] = 1
                if keyboard.is_pressed('a'):
                    cell[3] = 1
                if keyboard.is_pressed('s'):
                    cell[4] = 1
                if keyboard.is_pressed('d'):
                    cell[5] = 1
                if keyboard.is_pressed('enter'):
                    os.system('cls' if os.name == 'nt' else 'clear')
                    cell = tuple(cell)
                    barrers.append(cell)
                    print(barrers)
                    break
            time.sleep(0.1)
        if keyboard.is_pressed('#'):
            time.sleep(0.1)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(barrers)
            index = input('Digit the index of the item that you want to remove: ')
            index = int(index)
            print(f'Are you sure that you want to remove the item: {barrers[index]} (y/n)')
            decision = input()
            if decision == 'y':
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f'{barrers[index]} removed')
                del barrers[index]
                print(barrers)
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('Selection is on')

        if keyboard.is_pressed('control+s'):
            print('Do you want to save the data ?(y/n)')
            response = input()
            if response == 'y':
                for row in barrers:
                    database.insert_barrers(row)
                os.system('cls' if os.name == 'nt' else 'clear')
                print('Data is Saved !!')
                print('Selection is on')
                barrers = []
            else:
                os.system('cls' if os.name == 'nt' else 'clear')
                print('Selection is on')

        if keyboard.is_pressed('0'):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(barrers)
            print('Selecet the index of which item do you want to modify: ')
            index = input()
            index = int(index)
            print(f'Are you sure that you want to modify the item: {barrers[index]} (y/n) ?')
            decision = input()
            os.system('cls' if os.name == 'nt' else 'clear')
            if decision == 'y':
                new_item = input('Write de new item: ')
                print(f'{barrers[index]} -> {new_item}')
                print('Item modified !!')



        if keyboard.is_pressed('esc'):
            return barrers

database = Database()
for row in get_barrers():
    database.insert_barrers(row)

