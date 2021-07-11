# Autoloader
import sys
import os
from pathlib import Path

path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))


from pywinauto import application
import traceback
import win32gui
import win32process
from win32gui import SetForegroundWindow
from src.errors.character_errors import LoginError, RetryError
import time
import keyboard
from src.tools.search import Search
import pyautogui
import pytesseract
from pytesseract import Output
from PIL import ImageGrab
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# win32gui.ShowWindow(window[0],5)
# win32gui.SetForegroundWindow(window[0])
class Login:
    @staticmethod
    def open_new_dofus_window():
        try:
            app = application.Application()
            # dofus_application_path = f"{os.getenv('LOCALAPPDATA')}{os.sep}Ankama{os.sep}zaap{os.sep}dofus{os.sep}Dofus.exe"
            dofus_application_path = f"D:{os.sep}Ankama{os.sep}Dofus{os.sep}Dofus.exe"
            app.start(dofus_application_path)
            time.sleep(15)
        except:
            raise LoginError("Can't open dofus.exe")

    @staticmethod
    def get_dofus_windows_handle():
        def windowEnumerationHandler(hwnd, all_windows):
            all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        all_windows = list()
        win32gui.EnumWindows(windowEnumerationHandler, all_windows)
        for window in all_windows:
            # print(window)
            if re.search(r"(^Dofus\s\d\.\d{1,2}\.\d{1,2}\.\d{1,2}$)", window[1]):
                return window[0]
        raise LoginError("Can't find dofus.exe window")

    @staticmethod
    def login(account, window_id, screen_size):
        pyautogui.press("alt")
        win32gui.ShowWindow(window_id, 5)
        win32gui.SetForegroundWindow(window_id)
        search = Search()
        try:
            password_pos = Login.wait_and_get_login_possition(screen_size, search)
        except:
            raise LoginError("Can't find login possition")
        pyautogui.click(password_pos)
        Login.ctrl_a()
        keyboard.press_and_release("delete")
        pyautogui.click(password_pos)
        keyboard.write(account["password"])
        time.sleep(2)
        keyboard.press_and_release("tab")
        time.sleep(0.4)
        keyboard.write(account["login"])
        time.sleep(0.3)
        keyboard.press_and_release("enter")
        time.sleep(0.3)
        keyboard.press_and_release("enter")
        time.sleep(3)
        Login.select_character(
            character_name=account["name"],
            window_id=window_id,
            screen_size=screen_size,
            search=search,
        )

    @staticmethod
    def select_character(character_name, window_id, screen_size, search):
        region_to_search = (
            screen_size[0] * 0.20863836017,
            screen_size[1] * 0.39322916667,
            screen_size[0] * 0.4450951683748,
            screen_size[1] * 0.825520833333334,
        )
        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
                raise LoginError("Time out to find character")
            mathces = search.search_color(RGB=(255, 0, 255), region=region_to_search)
            if len(mathces) > 0:
                break
        characters_name_img = ImageGrab.grab(region_to_search)
        data = pytesseract.image_to_data(
            characters_name_img, output_type=Output.DICT, config="--psm 6 --oem 3"
        )
        try:
            character_name_index = data["text"].index(character_name)
        except:
            raise LoginError("Impossible to find character on list")
        xcoord, ycoord, width, height = (
            data["left"][character_name_index],
            data["top"][character_name_index],
            data["width"][character_name_index],
            data["height"][character_name_index],
        )
        pyautogui.doubleClick(
            (
                region_to_search[0] + xcoord + width / 2,
                region_to_search[1] + ycoord + height / 2,
            )
        )

    @staticmethod
    def ctrl_a():
        time.sleep(0.1)
        keyboard.press("control")
        time.sleep(0.01)
        keyboard.press_and_release("a")
        keyboard.release("control")
        time.sleep(0.2)

    @staticmethod
    def kill_window(window_id):
        pid = win32process.GetWindowThreadProcessId(window_id)[1]
        os.kill(pid, 15)

    @staticmethod
    def get_position_of_login_and_password(list_of_itens):
        max_xcoord = max(list_of_itens, key=lambda item: item[0])[0]
        x_coord = max_xcoord + abs(
            max_xcoord - min(list_of_itens, key=lambda item: item[0])[0]
        )
        min_ycoord = min(list_of_itens, key=lambda item: item[1])[1]
        y_coord = min_ycoord + (
            max(list_of_itens, key=lambda item: item[0])[1] - min_ycoord
        )
        return (x_coord, y_coord)

    @staticmethod
    def wait_and_get_login_possition(screen_size, search):
        region = (
            screen_size[0] * 0.25,
            screen_size[1] * 0.25,
            screen_size[0] * 0.75,
            screen_size[1] * 0.75,
        )
        start_time = time.time()
        while True:
            if time.time() - start_time > 60:
                raise LoginError("Impossible to find login position")
            keyboard.press_and_release("esc")
            time.sleep(1)
            password = search.search_color(RGB=(255, 0, 255), region=(region))
            if len(password) != 0:
                return Login.get_position_of_login_and_password(password)

    @staticmethod
    def run(account, screen_size):
        Login.open_new_dofus_window()
        window_id = Login.get_dofus_windows_handle()
        try:
            Login.login(account, window_id, screen_size)
        except LoginError as e:
            Login.kill_window(window_id)
            traceback.print_tb(e.__traceback__)
            raise RetryError("Fail to login")
        time.sleep(5)
        return window_id


if __name__ == "__main__":
    # def windowEnumerationHandler(hwnd, top_windows):
    #     all_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    # dofus_applications_ids = list()
    # all_windows = list()
    # win32gui.EnumWindows(windowEnumerationHandler, all_windows)
    # for window in all_windows:
    #     print(window)
    log = Logi.run({"login": "ee", "password": "Pepinous", "name": "Pepinous"})
