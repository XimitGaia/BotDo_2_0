# Autoloader
import sys
import os
import time
from pathlib import Path

path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

from abc import ABC, abstractmethod
from src.character.character import Character


class ActionInterface(ABC):
    @abstractmethod
    def run(self, character: Character):
        pass
