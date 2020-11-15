
from PIL import Image
from PIL import ImageGrab
import pytesseract
from search import Search
import time
import pyautogui

search = Search()
screen_size = ImageGrab.grab().size

bottom_region = (0,
            round(0.65*screen_size[1]),
            screen_size[0],
            screen_size[1]
            )

# image = Image.open("C:\\Users\\Lucas\\Desktop\\x\\src\\tools\\screen_markers\\name_marker.png")
# time.sleep(1)
# a = search.search_image(image=image, screen=bottom_region)
# region = (a[0][0] ,a[0][-1] + bottom_region[1],a[-1][0] ,a[-1][-1] + bottom_region[1] + 5)

# while True:
#     image2 = ImageGrab.grab(region)
#     print(pytesseract.image_to_string(image2, config='--psm 7'))
#     time.sleep(1)

image = Image.open("C:\\Users\\Lucas\\Desktop\\Untitled.png")
time.sleep(1)
a = search.search_image(image=image, screen=bottom_region)
while True:
    a = search.search_color(RGB=(76, 0, 61), region= bottom_region)
    if len(a) > 0:
        print('battle')
    else:
        print('normal')
