# Autoloader
import sys
import os
import time
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

from src.scheduler.actions.action_interface import ActionInterface
from src.character.character import Character


class MoveAction(ActionInterface):

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_position(self):
        return (self.x, self.y)

    def run(self, character: Character):
        character.go_to(self.get_position())

