# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))

from src.screen_controllers.screen import Screen
import keyboard
import time
import re

class Chat:

    def __init__(self, screen: Screen, character_name):
        self.screen = screen
        self.character_name = character_name
        self.chat_position =  None
        self.cicle_list = [
            'Trabalho quenem um cavalo, e nada de dinheiro...',
            'Vou coletando feliz os meus recursos',
            'Sou um trabalhador Brasileiro',
            'Bora trabalhar logo logo vem os mk',
            'Ja to aqui a umas 2h e essa prof n upa ASHAHSHASH',
            'Aff queria ser rico já...',
            'Quer saber uma coisa engracada !? Tok Tok...',
            'Ai!',
            'A caminho de Belém, frigost!',
            'Jesus morou na casinha do Gobal',
            'To coletando desde o 1.29 e n fico rico'
        ]
        self.get_chat_position()
        self.get_chat_content()

    def minimize_chat(self):
        keyboard.press('alt')
        time.sleep(0.1)
        keyboard.press_and_release('-')
        keyboard.release('alt')
        time.sleep(0.1)

    def maximize_chat(self):
        keyboard.press_and_release('+')

    def get_chat_position(self):
        width_constant = 0.287941787941
        chat_input_height_const = 0.02639296187
        chat_height_const = 0.3504398826979
        input_height = round(self.screen.game_active_screen[3] * chat_input_height_const)
        chat_width = round(width_constant * (self.screen.game_active_screen[2] - self.screen.game_active_screen[0]))
        chat_height = round(self.screen.game_active_screen[3] * chat_height_const)
        xcoord = self.screen.game_active_screen[0]
        ycoord = self.screen.screen_size[1] - (chat_height + input_height)
        self.chat_position = (xcoord, ycoord, xcoord + chat_width, ycoord + chat_height)

    def filter_chat_info(self, text):
        filter_text = f'{self.character_name}:(.+)'
        filtered_text = re.findall(filter_text, text)
        return [text.strip() for text in filtered_text]

    def get_chat_content(self):
        text = self.screen.get_chat_content(self.chat_position)
        filtered_text = self.filter_chat_info(text)
        if filtered_text == []:
            text = self.screen.get_chat_content(self.chat_position, ocr_config_number=2)
            filtered_text = self.filter_chat_info(text)
        return filtered_text

    def chat_io(self, string_array):
        self.maximize_chat()
        keyboard.press_and_release('space')
        time.sleep(0.5)
        keyboard.write('/clear')
        time.sleep(0.5)
        keyboard.press_and_release('enter')
        time.sleep(0.5)
        for item in string_array:
            keyboard.write(item)
            time.sleep(0.5)
            keyboard.press_and_release('enter')
            time.sleep(0.5)
        time.sleep(1.0)
        result = self.get_chat_content()
        keyboard.press_and_release('esc')
        time.sleep(0.5)
        self.minimize_chat()
        return result

    def refresh_frase(self):
        frase = self.cicle_list.pop(0)
        self.cicle_list.append(frase)
        self.chat_io([frase])


# time.sleep(2)
# s = Screen()
# c = Chat(s,'Pepinous')
# time.sleep(2)
# print(c.chat_io(['%hp%','%pos%']))