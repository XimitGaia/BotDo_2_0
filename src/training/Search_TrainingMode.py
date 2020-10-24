import win32api
import time
import random
from PIL import Image
from PIL import ImageGrab
import os
import numpy as np
import colorsys

class Search:
    
    @staticmethod
    def search(image,screen,pos_list = [],match_tolerance=0,color_tolerance = 0.02, validator_group_porcentage = 0,saturation_tolerance = 0, bright_tolerance = 0 ):#match_tolerance (0 - 1) 0 means exactly the same, screen = (x1,y1,x2,y2) rectangle top left, button right 
        start = time.time()
        img = image
        screen = screen
        img_HSV = img.convert('HSV')#cria copia rgb
        screen_HSV = screen.convert('HSV')
        valid_pixels = Search.get_valid_pixels(img) #pixels a serem comparados
        rest_group , validator_group = Search.get_validator_group(valid_pixels, validator_group_porcentage= validator_group_porcentage)
        reference_point = (0,0)
        reference_match_area = Search.get_reference_match_area(reference_point,img.size,screen.size)
        acuracy_list = []
        miss_match = 0
        exact_match = 0
        validated = True
        for x in range(reference_match_area[0][0],reference_match_area[1][0]+1):
            for y in range(reference_match_area[0][1],reference_match_area[1][1]+1):
                validator_error = 0 #quantos pixels
                for pos in validator_group:
                    validated = True
                    if not Search.check_color_renge(img_HSV.getpixel(pos),screen_HSV.getpixel((x+pos[0],y+pos[1])), color_tolerance, saturation_tolerance = saturation_tolerance , bright_tolerance = bright_tolerance):
                        validator_error += 1
                        if validator_error >= round(len(validator_group)*match_tolerance):
                            validated = False
                            break
                if validated:
                    match_error = 0
                    for pos in rest_group:
                        match = True
                        if not Search.check_color_renge(img_HSV.getpixel(pos),screen_HSV.getpixel((x+pos[0],y+pos[1])), color_tolerance):
                            match_error += 1
                            if match_error >= round(len(rest_group) * match_tolerance):
                                match = False
                                break
                    if match:
                        if (x,y) in pos_list:
                            exact_match +=1
                        else:
                            miss_match += 1
        return  exact_match, miss_match , time.time() - start



    @staticmethod
    def get_valid_pixels(image):
        img = image
        matrix = np.array(img)#!!!!!!!!!!!!!!!!!!!! arrumar - ver: https://stackoverflow.com/questions/38198379/how-to-change-the-pixel-values-of-an-image
        px , py = img.size
        valid_pixels = []
        for pixel_y in range(py - 1): # Atention Matrix[a][b] = pixel(b,a)
            for pixel_x in range(px - 1):
                if image.mode == 'RGB' or matrix[pixel_y][pixel_x][3] == 255:
                    valid_pixels.append((pixel_x,pixel_y))
        return valid_pixels
    
    @staticmethod
    def get_validator_group(valid_pixels,validator_group_porcentage = 0.05):
        rest_group = valid_pixels
        min_match = round(len(valid_pixels)*validator_group_porcentage)
        validator_group = list()
        for i in range(min_match):
            random_position = random.randint(0,len(rest_group)-1)
            validator_group.append(rest_group[random_position])
            rest_group.pop(random_position)
        return rest_group, validator_group

    @staticmethod
    def get_reference_match_area(reference_point,image_size,screen_size):
        x_top_left,y_top_left = reference_point
        x_right_down = screen_size[0] - (image_size[0] - x_top_left)
        y_right_down = screen_size[1] - (image_size[1] - y_top_left)
        return [(x_top_left,y_top_left),(x_right_down,y_right_down)]

    @staticmethod
    def check_color_renge(pixel_1_HSV,pixel_2_HSV,color_tolerance,saturation_tolerance = 0.05,bright_tolerance = 0.5):
        H1 , S1 , V1 = pixel_1_HSV # get pixel HSV values
        H2 , S2 ,  V2 = pixel_2_HSV
        Hdelta = round(color_tolerance*42.5)
        Hdist = abs(H1-H2)
        if abs(S1-S2) <= round(saturation_tolerance * 255):
            if abs(V1-V2) <= round(bright_tolerance * 255):
                if (255-Hdelta <= Hdist or Hdist <= Hdelta):
                    return True
        return False
