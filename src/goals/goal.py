# Autoloader
import sys
import os
import time
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

from abc import ABC, abstractmethod
from src.scheduler.actions.action_interface import ActionInterface


class Goal(ABC):

    @abstractmethod
    def get_next_step(self, character_name: str) -> ActionInterface:
        pass
