# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])

# Import system
from bs4 import BeautifulSoup
import requests
import time


class Character:

    def __init__(self, character_name, character_id):
        self.character_name = character_name
        self.character_id = character_id
        self.character_page_url = self.get_character_page_url(self.character_name)
        #self.character_professions

    def get_character_page_url(self, character_name):
        search_url = f'https://www.dofus.com/en/mmorpg/community/directories/character-pages?text={character_name}&character_homeserv%5B%5D=202&character_level_min=0&character_level_max=2340'
        result = requests.get(search_url)
        if result.status_code == 200:
            soup = BeautifulSoup(result.text, 'html.parser')
            characters_result = soup.select('.ak-responsivetable > tbody > tr > td:nth-of-type(2) > a[href]')
            for character in characters_result:
                if character.text == character_name:
                    return f'https://www.dofus.com{character["href"]}'

    # def get_character_professions(self, character_page_url):


c = Character('Bombaastic',1515)
print(c.character_page_url)