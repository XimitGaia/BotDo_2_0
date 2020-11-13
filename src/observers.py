import time
from PIL import Image
from src.tools.search import Search




class Observers:

    def __init__(self, screen , state):
        search = Search()
        battle_observer(search)

    @staticmethod
    def battle_observer(search):
        while True:
            if len(search.search_image())