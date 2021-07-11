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
    def __init__(self, map_id: int):
        self.map_id = map_id

    def get_map_id(self):
        return self.map_id

    def run(self, character: Character):
        character.go_to(self.get_map_id())
