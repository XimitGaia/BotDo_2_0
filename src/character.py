# Autoloader
import sys
import os
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[1]))
root_path = str(path.parents[1])

# Import system
from bs4 import BeautifulSoup
from src.state.state import State
from src.screen import Screen
from src.login import Login
import requests
import time


class Character:

    def __init__(
        self,
        state: State,
        screen: Screen,
        account: dict
    ):
        self.shared_state = state
        self.screen = screen
        self.name = None
        self.login = None
        self.password = None
        self.window_id = None
        self.level = None
        self.class_name = None
        self.primary_status = dict()
        self.res_status = dict()
        self.secundary_status = dict()
        self.damage_status = dict()
        self.skills = dict()
        self.queue = list()
        self.load_metadata(account)
        self.queue.append(self.login_dofus)

    def run_function(self):
        if len(self.queue) > 0:
            job = self.queue.pop(0)
            if job:
                job()
        self.shared_state.set_state(key='turn_off', value='free')

    def login_dofus(self):
        login = Login(screen_size=self.screen.screen_size)
        self.window_id = login.run(
            accounts=[{
                'login': self.login,
                'password': self.password,
                'name': self.name
            }]
        )[0]

    def check_health(self):
        print('dwdwdwdw')

    def load_metadata(self, account: dict):
        self.load_damages(account.get('damage'))
        self.class_name = account.get('class')
        self.level = account.get('level')
        self.name = account.get('name')
        self.login = account.get('login')
        self.password = account.get('password')
        self.load_primary_status(account.get('primaryCharacteristics'))
        self.load_resistances(account.get('resistences'))
        self.load_secundary_status(account.get('secundaryCharacteristics'))

    def load_damages(self, damage: dict):
        dict_damages = {
            "Air (fixed)": "air_fixed",
            "Critical damage": "critical damage",
            "Damage": "damage",
            "Earth (fixed)": "earth_fixed",
            "Fire (fixed)": "fire_fixed",
            "Neutral (fixed)": "neutral_fixed",
            "Pushback": "pushback",
            "Reflect": "reflect",
            "Traps (Power)": "traps_power",
            "Traps (fixed)": "traps_fixed",
            "Water (fixed)": "water_fixed",
        }
        if damage:
            for item in damage:
                self.damage_status[dict_damages.get(item)] = damage.get(item)

    def load_resistances(self, resistances):
        dict_resistances = {
                "Air (%)": "air",
                "Air (fixed)": "air_fixed",
                "Critical Hits (fixed)": "critical_hits_fixed",
                "Earth (%)": "earth",
                "Earth (fixed)": "earth_fixed",
                "Fire (%)": "fire",
                "Fire (fixed)": "fire_fixed",
                "Neutral (%)": "neutral",
                "Neutral (fixed)": "neutral_fixed",
                "Pushback (fixed)": "pushback_fixed",
                "Water (%)": "water",
                "Water (fixed)": "water_fixed"
        }
        if resistances:
            for item in resistances:
                self.res_status[dict_resistances.get(item)] = resistances.get(item)

    def load_primary_status(self, primary_status: dict):
        if primary_status:
            for item in primary_status:
                self.primary_status[item.lower()] = primary_status.get(item)

    def load_secundary_status(self, secundary_status: dict):
        dict_secundary_status = {
            "AP Parry": "ap_parry",
            "AP Reduction": "ap_reduction",
            "Dodge": "dodge",
            "Heals": "heals",
            "Initiative": "initiative",
            "Lock": "lock",
            "MP Parry": "mp_parry",
            "MP Reduction": "mp_reduction",
            "Prospecting": "prospecting",
            "Summons": "summons"
        }
        if secundary_status:
            for item in secundary_status:
                self.secundary_status[dict_secundary_status.get(item)] = secundary_status.get(item)



