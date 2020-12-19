# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))


# Import system
from src.tools.replace_files import replace_files
from database.sqlite import Database
from src.goals.resource import Resource
from src.state.state import State
from src.resolver import Resolver
from src.screen import Screen
from src.observers import Observers
from src.login import Login
import time
import json
import pyautogui


josn_str = sys.argv[1].replace("?", '"')
args = json.loads(josn_str)
accounts = args['accounts']
selects = args['selects']

debug = 1 #bool(int(input('debug:')))
print('Initialize database module')
database = Database()
print('Changing files')
if not debug:
    replace_files()
print('Initialize Screen module')
screen = Screen()
print('Initialize State module')
state = dict({'status': 'initializing'})
state = State(state=state, debug=debug)
print('Initialize Observers')
Observers.battle_observer(screen=screen,state=state,debug=debug)
print('Loading Accounts')
login = Login(accounts,screen.screen_size)
