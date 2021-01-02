from PIL import Image
from PIL import ImageGrab
import pyautogui
import time


def get_chat_size(game_active_screen,screen_size):
        width_constant = 0.287941787941
        width = width_constant * (game_active_screen[2] - game_active_screen[0])
        xcoord = game_active_screen[0]
        marge_const = 0.02639296187
        marge = marge_const * game_active_screen[3]
        pyautogui.moveTo((xcoord,screen_size[1] - marge))
        time.sleep(1)
        pyautogui.moveTo((xcoord + width,screen_size[1] - marge))
        return

def teste():#(x1,y1,x2,y2)
    screen_size = ImageGrab.grab('').size
    screen_proportion = 0.704
    action_screen_proportion = 0.709
    width = screen_size[0]*screen_proportion
    X = (screen_size[0] - width)/2
    high = action_screen_proportion * width
    game_active_screen = (
        round(X),
        0,
        round(X+width),
        round(0+high)
    )
    print(game_active_screen)
    get_chat_size(game_active_screen,screen_size)



teste()