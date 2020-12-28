# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))


# Import system
import time
from PIL import Image
from PIL import ImageGrab
from src.tools.search import Search
import threading
from src.state.state import State
from src.screen import Screen
import keyboard


class Observers:

    debug_map = dict({
        'battle': True
    })

    @staticmethod
    def battle_observer(screen:Screen, state:State, debug: bool= False):
        #print('to aqui')
        def run():
            if debug:
                counter = 0
            not_found_count = 0
            state.set_thread_status('battle_observer_thread', 'running')
            while True:
                if state.get('status') == 'paused':
                    state.set_thread_status('battle_observer_thread', 'paused')
                    while True:
                        if state.get('status') != 'paused':
                            state.set_thread_status('battle_observer_thread', 'runnning')
                            break
                        time.sleep(1)
                if debug and Observers.debug_map.get('battle'):
                    print(f'tick battle observer, total: {counter}')
                    counter += 1
                    print(f'state.is_bussy -> {state.is_bussy}')
                    print(state.state)
                match_list = Search.search_color(RGB=(76, 0, 61), region=screen.fight_buttom_region)
                if len(match_list) > 0:
                    state.set_state(key='status', value='battle')
                    not_found_count = 0
                elif state.get('status') == 'battle':
                    not_found_count += 1
                if not_found_count > 10:
                    state.is_bussy = False
                    state.set_state(key='status', value='')
                time.sleep(0.2)

        battle_observer_thread = threading.Thread(target=run, args=())
        battle_observer_thread.daemon = True
        battle_observer_thread.start()

    @staticmethod
    def pause_trigger_observer(state:State, debug:bool=False):
        def run():
            state.set_thread_status('pause_trigger_observer_thread', 'running')
            while True:
                if keyboard.is_pressed('control + p'):
                    state.pause_resume_state(pause_resume='pause')
                if keyboard.is_pressed('control + r'):
                    state.pause_resume_state(pause_resume='resume')
                # if debug:
                #     if state.get('status') == 'paused':
                #         print(state.get('threads_status'))
            time.sleep(0.2)

        pause_trigger_observer_thread = threading.Thread(target=run, args=())
        pause_trigger_observer_thread.daemon = True
        pause_trigger_observer_thread.start()

