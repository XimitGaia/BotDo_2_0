#Ferramentas
import pyautogui
import pytesseract  
import keyboard
import win32api
import time
import wx
import cv2
from PIL import ImageGrab
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class Ferramentas:
    
    @staticmethod
    def get_area_info():
        print('Press CTRL+ALT to select the two points to define a rectangle')
        print('point 1:')
        point_1 = Ferramentas.get_mouse_position() #pega posicao do clique 1
        time.sleep(0.3)
        print('point 2:')
        point_2 = Ferramentas.get_mouse_position() #pega posicao do clique 2
        X = min(point_1[0],point_2[0])
        Y = min(point_1[1],point_2[1])
        Ferramentas.print_a_retangle((X,Y),(abs(point_2[0]-point_1[0]),abs(point_2[1]-point_1[1])))
        print('X:', X, ';', 'Y:', Y, ';', 'Width:', abs(point_2[0]-point_1[0]), ';', 'High:', abs(point_2[1]-point_1[1]))
        print('Press CTRL + S to salve a .txt file, or esc to exit: ')
        while True:
            if keyboard.is_pressed('esc'):
                break
            if keyboard.is_pressed('control+s'):
                print('saved')
                break

    @staticmethod
    def print_a_retangle(pos,size):
        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR |
                  wx.NO_BORDER | wx.FRAME_SHAPED  )
        region = wx.Frame(None, title='',pos = pos ,size = size, style = style)
        region.SetTransparent( 700 )
        region.Show(True)
        print('Press esc to exit: ')
        while True:
            if keyboard.is_pressed('esc'):
                break
        region.Show(False)
    
    @staticmethod
    def get_mouse_position():
        while True:  # making a loop
            try:  # used try so that if user pressed other than the given key error will not be shown
                if keyboard.is_pressed('control+alt'):  # if key 'q' is pressed
                    print(pyautogui.position())
                    return pyautogui.position()
                    break
                if keyboard.is_pressed('esc'):
                    break
            except:
                continue  # if user pressed a key other than the given key the loop will break
    
    @staticmethod            
    def show_matches_on_screen(image):
        print('press CTRL+SHIFT to start')
        time.sleep(2)
        matches_position = pyautogui.locateAllOnScreen(image)
        for match in matches_position:
            image_position = list(match)
            Ferramentas.print_a_retangle((image_position[0],image_position[1]), (image_position[2],image_position[3]))
        time.sleep(3)
        
    @staticmethod
    def get_image_first_info(image):
        picture = cv2.imread(image)
        #print('Width:', size[1],';', 'High:', size[0] , ';', 'Pixels number:', picture.size)
        return {'whidth': picture.shape[1] , 'high': picture.shape[0], 'pixel_number': picture.size}
    
    @staticmethod
    def resize_untill_find(image,bigger_or_smaller, min_size = 50 , max_size = 150 , one_match_per_point = 'on'): #(imagem, diminuir ou aumentar, min_size = reduzir ate X%, 30 significa reduzir 70% do tam original, max_size = aumentar até X%)
        print('Press CTRL+ALT to start:')
        while True:
            if keyboard.is_pressed('control+alt'):
                break
        print(time.time())
        image_info = Ferramentas.get_image_first_info(image)
        image = cv2.imread(image)
        cv2.imshow('b',image)
        image_rate = image_info['whidth'] / image_info['high'] #proporcao Width/High
        ocurrencies = {} # ocorrencias [x,y,w,h]
        match_number = 1 # numero da ocorrencia
        high = image_info['high']
        if bigger_or_smaller == 'smaller':
            while int((high/image_info['high'])*100) >= int(min_size):
                #print('{}%'.format(round((high/image_info['high'])*100)))
                width = round(image_info['whidth']-((image_info['high'] - high) * image_rate))
                dimension = (width,high) # nova dimensao da imagem
                #print('Dimension:', dimension)
                image_resized = cv2.resize(image,dimension) #muda tamanho apra dimensao nova
                if one_match_per_point == 'off':
                    matches_position = pyautogui.locateAllOnScreen(image_resized, confidence = 0.99) # lista todos os matches 90% iguais ao da imagem redimensionada
                    for region in matches_position:
                        region = list(region)
                        ocurrencies['Match_{}'.format(match_number)] = region # region = [X,Y, new_Width , new_High]
                        match_number += 1 
                if one_match_per_point == 'on':
                    match_position = pyautogui.locateOnScreen(image_resized, confidence = 0.99)
                    if match_position != None:
                        match_position = list(match_position)
                        ocurrencies['Match_{}'.format(match_number)] = match_position # region = [X,Y, new_Width , new_High]
                        match_number += 1
                high -= 1
        if bigger_or_smaller == 'bigger':
            while int((high/image_info['high'])*100) <= int(max_size):
                print('{}%'.format(round((high/image_info['high'])*100)))
                width = round(image_info['whidth']+((high - image_info['high']) * image_rate))
                dimension = (width,high) # nova dimensao da imagem
                print('Dimension:', dimension)
                image_resized = cv2.resize(image,dimension) #muda tamanho apra dimensao nova
                if one_match_per_point == 'off':
                    matches_position = pyautogui.locateAllOnScreen(image_resized, confidence = 0.9) # lista todos os matches 90% iguais ao da imagem redimensionada
                    for region in matches_position:
                        region = list(region)
                        ocurrencies['Match_{}'.format(match_number)] = region # region = [X,Y, new_Width , new_High]
                        match_number += 1   
                if one_match_per_point == 'on':
                    match_position = pyautogui.locateOnScreen(image_resized, confidence = 0.9)
                    if match_position != None:
                        match_position = list(match_position)
                        ocurrencies['Match_{}'.format(match_number)] = match_position # region = [X,Y, new_Width , new_High]
                        match_number += 1 
                high += 1
        print(ocurrencies)
        print(time.time())
        cv2.waitKey(0)
        return ocurrencies
   
    @staticmethod
    def get_pixel_color():
        print('press CTRL+ALT to get the pixel RGB value under mouse cursor')
        position = Ferramentas.get_mouse_position()
        image = ImageGrab.grab()
        color = image.getpixel(position)
        print('(R,G,B):',color)
        print('Press esc to exit or enter to get more colors: ')
        while True:
            if keyboard.is_pressed('esc'):
                break
            if keyboard.is_pressed('enter'):
                Ferramentas.get_pixel_color()

    @staticmethod
    def print_ocurrencies_on_screen(image,big_or_small,min_size = 50,max_size = 150 , one_match_per_point = 'on'):
        match_list = Ferramentas.resize_untill_find(image, big_or_small, min_size= min_size, max_size = max_size ,one_match_per_point = 'on')
        for region in match_list:
            Ferramentas.print_a_retangle((match_list[region][0],match_list[region][1]), (match_list[region][2],match_list[region][3]))
        #Ferramentas.print_a_retangle((match_list['Match_5'][0],match_list['Match_5'][1]), (match_list['Match_5'][2],match_list['Match_5'][3]))

    @staticmethod
    def show_text_ocurrencies_on_image(image):
        image = cv2.imread(image)
        h, w, c = image.shape
        boxes = pytesseract.image_to_boxes(image) 
        for b in boxes.splitlines():
            b = b.split(' ')
            image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
        cv2.imshow('image', image)
        print('Press CTRL + S to salve a .txt file, or esc to exit: ')
        while True:
            if keyboard.is_pressed('esc'):
                break
            if keyboard.is_pressed('control+s'):
                print('saved')
                break

while True: 
    os.system('cls' if os.name == 'nt' else 'clear')
    app = wx.App()
    print(
        """
        _   _   _ _____ ___        __  __    _  _____ ___ ___  _   _ 
       / \ | | | |_   _/ _ \      |  \/  |  / \|_   _|_ _/ _ \| \ | |
      / _ \| | | | | || | | |_____| |\/| | / _ \ | |  | | | | |  \| |
     / ___ \ |_| | | || |_| |_____| |  | |/ ___ \| |  | | |_| | |\  |
    /_/   \_\___/  |_| \___/      |_|  |_/_/   \_\_| |___\___/|_| \_|                                                                  
 
    By Lucas Sievers
    """
    )
    print('SELECT ONE OF THE OPTIONS')
    print('1- get_area_info')
    print('2- get_image_first_info')
    print('3- show_matches_on_screen')
    print('4- resize_untill_find')
    print('5- get_pixel_color')
    print('6- print_ocurrencies_on_screen')
    print('7- show_text_ocurrencies_on_image')
    print('8- highlight (x,y),(w,d) : ')
    option = int(input("Select what you want: "))
    if option == 1:
        Ferramentas.get_area_info()
        app = None

    elif option == 2:
        image_path = input('Give the image path: ')
        Ferramentas.get_image_first_info(image_path)

    elif option == 3:
        image_path = input('Give the image path: ')
        Ferramentas.show_matches_on_screen(image_path)

    elif option == 4:
        image_path = str(input('Give the image path: '))
        reduce_or_expand = str(input('smaller or bigger: '))
        min_size = input('min_size: ')
        max_size = input('max_size: ')
        one_match_per_point = input('one_match_per_point(on/off): ')
        Ferramentas.resize_untill_find(image_path,reduce_or_expand,min_size = min_size, max_size = max_size, one_match_per_point = one_match_per_point)


    elif option == 5:
        Ferramentas.get_pixel_color()

    elif option == 6:
        image_path = str(input('Give the image path: '))
        reduce_or_expand = str(input('smaller or bigger: '))
        min_size = input('min_size: ')
        max_size = input('max_size: ')
        one_match_per_point = input('one_match_per_point(on/off): ')
        Ferramentas.print_ocurrencies_on_screen(image_path,reduce_or_expand,min_size = min_size, max_size = max_size, one_match_per_point = one_match_per_point)

    elif option == 7:
        image_path = str(input('Give the image path: '))
        Ferramentas.show_text_ocurrencies_on_image(image_path)

    elif option == 8:
        x_coord = int(input('input x coordinate: '))
        y_coord = int(input('input y coordinate: '))
        widith = int(input('widith of retangle: '))
        high = int(input('high of rectangle: '))
        Ferramentas.print_a_retangle((x_coord,y_coord),(widith,high))
        cv2.waitKey(0)

    elif option == -1:
        break


