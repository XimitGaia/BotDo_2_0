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
from src.character import Character
from src.observers import Observers
from src.orchestrator import Orchestrator
import time
import json
import pyautogui

# josn_str = sys.argv[1].replace("?", '"')
# args = json.loads(josn_str)
# accounts = args['accounts']
# selects = args['selects']

def run(api_data):
    accounts_meta_data = api_data['accounts']
    accounts = dict()
    mode = api_data['mode']
    selects = api_data['selects']
    print(accounts_meta_data)
    print()
    print(mode)
    print()
    print(selects)
    debug = 1 #bool(int(input('debug:')))
    print('Initialize database module')
    database = Database()
    print('Changing files')
    if not debug:
        replace_files()
    print('Initialize Screen module')
    screen = Screen()
    print('Initialize State module')
    state = dict({'status': 'initializing', 'threads_status':{}, 'turn_off': None})
    state = State(state=state, debug=debug)
    print('Initialize Observers')
    # Observers.pause_trigger_observer(state=state, debug=debug)
    # Observers.battle_observer(screen=screen, state=state, debug=debug)
    print('Loading Accounts')
    for account in accounts_meta_data:
        accounts[account.get('name')] = Character(
            state=state,
            screen=screen,
            account=account,
            database=database
        )
    goal_generator = Resource(database=database, resources=selects) if mode == 'resources' else None
    goal = goal_generator.run()
    orchestrator = Orchestrator(accounts=accounts, state=state)
