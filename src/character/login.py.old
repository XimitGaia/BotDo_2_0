# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))


from pywinauto import application
import win32gui
import win32process
from win32gui import SetForegroundWindow
import time
import keyboard
from src.tools.search import Search
import pyautogui
import pytesseract
from pytesseract import Output
from PIL import ImageGrab
import re








# win32gui.ShowWindow(window[0],5)
# win32gui.SetForegroundWindow(window[0])
class Login:

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.search = Search()
        self.characters = dict()
        self.dofus_applications_ids = list()



    def open_new_dofus_window(self,number_of_windows):
        for i in range(0,number_of_windows):
            app = application.Application()
            dofus_application_path = f"{os.getenv('LOCALAPPDATA')}{os.sep}Ankama{os.sep}zaap{os.sep}dofus{os.sep}Dofus.exe"
            app.start(dofus_application_path)
            time.sleep(3)


    def get_dofus_windows_handle(self):
        def windowEnumerationHandler(hwnd, all_windows):
            all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
        all_windows = list()
        win32gui.EnumWindows(windowEnumerationHandler, all_windows)
        for window in all_windows:
            if re.search(r'(^D?d?ofus \d+?.?\d+)',window[1]):
                self.dofus_applications_ids.append(window[0])

    def login(self,account):
        self.dofus_applications_ids
        account_id = self.dofus_applications_ids.pop()
        self.characters.update({account['name']: account_id})
        pyautogui.press('alt')
        win32gui.ShowWindow(account_id,5)
        win32gui.SetForegroundWindow(account_id)
        try:
            login_pos, pass_pos = self.wait_and_get_login_possition()
        except:
            self.kill_window(account['name'])
            return None
        pyautogui.click(login_pos)
        self.select_all()
        keyboard.press_and_release('delete')
        pyautogui.click(login_pos)
        keyboard.write(account['login'])
        time.sleep(2)
        keyboard.press_and_release('tab')
        keyboard.write(account['password'])
        keyboard.press_and_release('enter')
        time.sleep(1)
        self.select_character(
            character_name=account['name'],
            account_id=account_id
            )

    def select_character(self, character_name, account_id):
        region_to_search = (self.screen_size[0] * 0.20863836017, self.screen_size[1] * 0.39322916667,self.screen_size[0] * 0.4450951683748,self.screen_size[1] * 0.825520833333334)
        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
                self.kill_window(character_name)
                return None
            mathces = self.search.search_color(RGB=(255,0,255),region=region_to_search)
            if len(mathces) > 0:
                break
        characters_name_img = ImageGrab.grab(region_to_search)
        data = pytesseract.image_to_data(characters_name_img, output_type=Output.DICT, config ='--psm 6 --oem 3')
        try:
            character_name_index = data['text'].index(character_name)
        except:
            self.kill_window(character_name)
            return None
        xcoord, ycoord, width, height = (data['left'][character_name_index], data['top'][character_name_index], data['width'][character_name_index], data['height'][character_name_index])
        pyautogui.doubleClick((region_to_search[0] + xcoord + width/2, region_to_search[1]+ ycoord + height/2))

    def select_all(self):
        time.sleep(0.1)
        keyboard.press('control')
        keyboard.press_and_release('a')
        keyboard.release('control')
        time.sleep(0.2)

    def kill_window(self,character_name):
        account_id = self.characters[character_name]
        pid = win32process.GetWindowThreadProcessId(account_id)[1]
        os.kill(pid,15)
        del self.characters[character_name]

    def get_position_of_login_and_password(self,list_of_itens):
        max_xcoord = max(list_of_itens,key=lambda item:item[0])[0]
        x_coord = max_xcoord + abs(max_xcoord - min(list_of_itens,key=lambda item:item[0])[0])
        min_ycoord = min(list_of_itens,key=lambda item:item[1])[1]
        y_coord = min_ycoord + (max(list_of_itens,key=lambda item:item[0])[1] - min_ycoord)
        return (x_coord,y_coord)

    def wait_and_get_login_possition(self):
        region = (
            self.screen_size[0]*0.25,
            self.screen_size[1]*0.25,
            self.screen_size[0]*0.75,
            self.screen_size[1]*0.75
        )
        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
               return None
            keyboard.press_and_release('esc')
            time.sleep(1)
            password = self.search.search_color(RGB=(255,0,255),region=(region))
            if len(password) != 0:
                password = self.get_position_of_login_and_password(password)
                login = self.get_position_of_login_and_password(self.search.search_color(RGB=(0,255,255),region=(region)))
                return login, password

    def run(self, accounts):
        self.open_new_dofus_window(len(accounts))
        time.sleep(8)
        self.get_dofus_windows_handle()
        for account in accounts:
            self.login(account)
        time.sleep(2)
        return [self.characters[item] for item in self.characters]

if __name__ == "__main__":
    # def windowEnumerationHandler(hwnd, top_windows):
    #     all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    # dofus_applications_ids = list()
    # all_windows = list()
    # win32gui.EnumWindows(windowEnumerationHandler, all_windows)
    # for window in all_windows:
    #     print(window)
    log = Login([{'login': 'ee', 'password': 'Pepinous', 'name': 'Pepinous'}])