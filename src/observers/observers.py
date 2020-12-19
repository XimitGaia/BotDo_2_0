# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[2])

# Import system
import time
from src.tools.search import Search





class Observers:

    def __init__(self, screen , state):



    @staticmethod
    def battle_observer():
        while True:
            if len(search)