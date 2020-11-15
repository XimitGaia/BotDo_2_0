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


debug = bool(int(input('debug:')))
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
Observers.battle_observer(state=state,debug=debug)


while True: 
    #os.system('cls' if os.name == 'nt' else 'clear')
    print("""
     ____   ___  _____ _   _ ____    ____   ___ _____ 
    |  _ \ / _ \|  ___| | | / ___|  | __ ) / _ \_   _|
    | | | | | | | |_  | | | \___ \  |  _ \| | | || |  
    | |_| | |_| |  _| | |_| |___) | | |_) | |_| || |  
    |____/ \___/|_|    \___/|____/  |____/ \___/ |_|  
    By Lucas Sievers
    """
    )
    print('SELECT ONE OF THE OPTIONS')
    print('1  - Drop')
    print('2  - Resources')
    print('-1 - Exit')
    option = int(input("Select what you want: "))
    if option == 2: # drops options
        resource = Resource(database)
            


    elif option == -1:
        break
