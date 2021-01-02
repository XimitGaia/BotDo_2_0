# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

from src.screen import Screen





class Moving:

    def __init__(self, screen: Screen):
        self.screen = screen

    def get