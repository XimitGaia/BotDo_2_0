# Autoloader
import sys
import os
import time
from pathlib import Path

path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

from src.scheduler.actions.action_interface import ActionInterface
from src.character.character import Character


class HarvestAction(ActionInterface):
    def __init__(self, items: list):
        self.items = items

    def get_items(self) -> list:
        return self.items

    def run(self, character: Character):
        character.set_collect(self.get_items())
