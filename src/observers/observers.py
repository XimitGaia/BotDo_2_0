# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
# Import system
import time
import keyboard
import threading
import socket
from PIL import Image
from PIL import ImageGrab
from src.tools.search import Search
from src.state.state import State
from src.screen_controllers.screen import Screen


class Observers:

    debug_map = dict({
        'battle': True
    })

    @staticmethod
    def battle_observer(screen: Screen, state: State, debug: bool = False):
        def run():
            not_found_count = 0
            state.set_thread_status('battle_observer_thread', 'running')
            while True:
                State.check_pause_command(thread_name=battle_observer_thread)
                match_list = Search.search_color(RGB=(76, 0, 61), region=screen.fight_buttom_region)
                if len(match_list) > 10:
                    if state.get('status') != 'battle':
                        state.set_state(key='status', value='battle')
                    not_found_count = 0
                if state.get('status') == 'battle':
                    not_found_count += 1
                if not_found_count > 10:
                    state.set_state(key='status', value='running')
                time.sleep(0.2)

        battle_observer_thread = threading.Thread(target=run, args=())
        battle_observer_thread.daemon = True
        battle_observer_thread.start()

    @staticmethod
    def internet_observer(state: State):
        state.set_thread_status('internet_observer_thread', 'running')

        def checkInternetSocket(host="8.8.8.8", port=53, timeout=3):
            try:
                socket.setdefaulttimeout(timeout)
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
                return True
            except socket.error as ex:
                return False

        def run():
            while True:
                state.check_pause_command()
                internet = checkInternetSocket()
                if not internet:
                    state.set_state(key='status', value='disconnected')
                else:
                    if state.get('status') == 'disconnected':
                        state.set_state(key='status', value='reconnecting')
                time.sleep(2)

        internet_observer_thread = threading.Thread(target=run, args=())
        internet_observer_thread.daemon = True
        internet_observer_thread.start()

    @staticmethod
    def pause_trigger_observer(state: State, debug: bool = False):
        def run():
            state.set_thread_status('pause_trigger_observer_thread', 'running')
            while True:
                if keyboard.is_pressed('control + p'):
                    state.pause()
                if keyboard.is_pressed('control + r'):
                    state.resume()
            time.sleep(0.2)

        pause_trigger_observer_thread = threading.Thread(target=run, args=())
        pause_trigger_observer_thread.daemon = True
        pause_trigger_observer_thread.start()

