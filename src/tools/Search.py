import random
from PIL import Image
from PIL import ImageGrab
from PIL import PngImagePlugin
import os
import numpy as np
import colorsys
import typing
import time

class Search:
    
    @staticmethod
    def search(
        image: PngImagePlugin.PngImageFile,
        match_tolerance: float = 0.02,
        screen = '',
        color_tolerance: float = 0.02, 
        validator_group_porcentage: float = 0.05,
        saturation_tolerance: float = 0.05,
        bright_tolerance: float = 0.07,
        trainer: bool = False,
        resize: tuple = (0,0)

    )-> list:#screen = (x1,y1,x2,y2) rectangle top left, button right, all others parameters variate between 0 and 1
        if trainer == True:
            start_time = time.time()
        if trainer == False:
            screen = ImageGrab.grab(screen)#grab the screen ('' is fullscreen) or (x1,y1,x2,y2)
        #screen = Image.open("C:\\Users\\Lucas\\Desktop\\BotDo\\Training\\Screens\\screen_2.png")
        img = image
        if resize != (0,0):#check if image needs to be resized, and resize if needed
            img.thumbnail(resize, Image.ANTIALIAS)
        img_HSV = img.convert('HSV')#convert img to HSV
        screen_HSV = screen.convert('HSV')# convert screen to HSV
        total_matches = [] #list of total matches
        valid_pixels = Search._get_valid_pixels(image=img) #pixels a serem comparados
        rest_group , validator_group = Search._get_validator_group(
            valid_pixels=valid_pixels,
            validator_group_porcentage=validator_group_porcentage
        )
        reference_point = (0,0) #poin to use as reference when going trough the matrix
        reference_match_area = Search._get_reference_match_area(
            reference_point=reference_point,
            image_size=img.size,
            screen_size=screen.size
        )#area that the point of reference could be
        for x in range(reference_match_area[0][0],reference_match_area[1][0]+1):
            for y in range(reference_match_area[0][1],reference_match_area[1][1]+1):#go trough each pixel
                validator_error = 0 #number of pixels non-validated
                for pos in validator_group:# check some pixels of the image
                    validated = True
                    if not Search._check_color_renge(
                        pixel_1_HSV=img_HSV.getpixel(pos),
                        pixel_2_HSV=screen_HSV.getpixel((x+pos[0],y+pos[1])),
                        color_tolerance=color_tolerance,
                        saturation_tolerance=saturation_tolerance,
                        bright_tolerance=bright_tolerance 
                    ):# check the pixel are the same or similar
                        validator_error += 1
                        if validator_error >= round(len(validator_group)*match_tolerance):#if validation exeeds the number of non-validated pixels allowed it breaks
                            validated = False
                            break
                if validated:#if validated, start to try a match on the whole screen
                    match_error = 0
                    match = True
                    for pos in rest_group:
                        if not Search._check_color_renge(
                            pixel_1_HSV=img_HSV.getpixel(pos),
                            pixel_2_HSV=screen_HSV.getpixel((x+pos[0],y+pos[1])),
                            color_tolerance=color_tolerance,
                            saturation_tolerance=saturation_tolerance,
                            bright_tolerance=bright_tolerance 
                        ):
                            match_error += 1
                            if match_error >= round(len(rest_group) * match_tolerance):
                                match = False
                                break
                    if match:
                        total_matches.append((x,y))
        if trainer == True:
            total_time = float(time.time() - start_time)
            return total_matches, total_time
        return total_matches    


    @staticmethod
    def _get_valid_pixels(image: PngImagePlugin.PngImageFile)-> list: #get the pixels that has no transparency
        img = image
        matrix = np.array(img)#trnasform image in a matrix of pixels
        px , py = img.size
        valid_pixels = list()
        for pixel_y in range(py - 1): # Atention Matrix[a][b] = pixel(b,a)
            for pixel_x in range(px - 1):
                if image.mode == 'RGB' or matrix[pixel_y][pixel_x][3] == 255:
                    valid_pixels.append((pixel_x,pixel_y))
        return valid_pixels
    
    @staticmethod
    def _get_validator_group(valid_pixels: list,validator_group_porcentage:float = 0.05):# get some piexels to pre-validate the image
        rest_group = valid_pixels
        min_match = round(len(valid_pixels)*validator_group_porcentage)
        validator_group = list()
        for i in range(min_match):
            random_position = random.randint(0,len(rest_group)-1)
            validator_group.append(rest_group[random_position])
            rest_group.pop(random_position)
        return rest_group, validator_group

    @staticmethod
    def _get_reference_match_area(
        reference_point: tuple,
        image_size: tuple,
        screen_size: tuple
    )-> list:#area that the reference point is allowed
        x_top_left,y_top_left = reference_point
        x_right_down = screen_size[0] - (image_size[0] - x_top_left)
        y_right_down = screen_size[1] - (image_size[1] - y_top_left)
        return [(x_top_left,y_top_left),(x_right_down,y_right_down)]

    @staticmethod
    def _check_color_renge(
        pixel_1_HSV: tuple,
        pixel_2_HSV: tuple,
        color_tolerance: float,
        saturation_tolerance: float = 0.05,
        bright_tolerance: float = 0.1
    )-> bool:
        H1 , S1 , V1 = pixel_1_HSV # get pixels HSV values
        H2 , S2 ,  V2 = pixel_2_HSV
        Hdelta = round(color_tolerance*42.5) #42.5 force the color to stay in its range (remember 255+x = x for x< 255, like a circle) red [234-21] yellow [21-64] green [64-106] cian[106-149] blue [149-191] cian [191-234]
        Hdist = abs(H1-H2)
        if abs(S1-S2) <= round(saturation_tolerance * 255):
            if abs(V1-V2) <= round(bright_tolerance * 255):
                if (255-Hdelta <= Hdist or Hdist <= Hdelta):# check if the clors area in the delta range
                    return True
        return False

if __name__ == '__main__':
    import keyboard
    img = Image.open("C:\\Users\\Lucas\\Desktop\\resist_test\\01.png")
    img.thumbnail((5,5), Image.ANTIALIAS)
    while True:
        if keyboard.is_pressed('control+alt'):
            print('Started')
            break
    #print(img.size)
    print(Search.search(image=img,screen=(0,608,1365,767)))



