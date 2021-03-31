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
from src.scheduler.resolver import Resolver
from src.screen_controllers.screen import Screen
from src.character.character import Character
from src.observers.observers import Observers
from src.scheduler.orchestrator import Orchestrator
from src.scheduler.account_and_goal import AccountAndGoal
import time
import json
import pyautogui

# josn_str = sys.argv[1].replace("?", '"')
# args = json.loads(josn_str)
# accounts = args['accounts']
# selects = args['selects']

def run(api_data):
    accounts = dict()
    debug = 1 #bool(int(input('debug:')))
    print('Initialize database module')
    database = Database()
    print('Changing files')
    if not debug:
        replace_files()
    print('Initialize Screen module')
    screen = Screen()
    print('Initialize State module')
    state = dict({'status': 'initializing', 'threads_status':{}, 'turn_of': None})
    state = State(state=state, debug=False)
    print('Initialize Observers')
    # Observers.pause_trigger_observer(state=state, debug=debug)
    # Observers.battle_observer(screen=screen, state=state, debug=debug)
    print('Loading Accounts')

    accounts = list()
    for goal_and_accounts in api_data:
        # Fron enviara accounts + items para cada account.
        mode = goal_and_accounts.get('mode')
        if mode == 'resources':
            goal = Resource(
                database=database,
                resources=goal_and_accounts.get('items'),
                account_number=len(goal_and_accounts.get("accounts"))
            )
        else:
            goal = None
        for accoun_data in goal_and_accounts.get("accounts"):
            account = Character(
                state=state,
                screen=screen,
                account=accoun_data,
                database=database
            )
            accounts.append(AccountAndGoal(account, goal))

    Orchestrator(account_and_goals=accounts, state=state)
