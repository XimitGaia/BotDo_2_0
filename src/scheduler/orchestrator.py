# Autoloader
import sys
import os
import time
import threading
from pathlib import Path

path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))
from src.state.state import State
from typing import List
from src.errors.character_errors import JobError, CharacterCriticalError
from src.goals.goal import Goal
from src.scheduler.account_and_goal import AccountAndGoal


class Orchestrator:
    def __init__(self, account_and_goals: List[AccountAndGoal], state: State):
        self.accounts = self.format_accounts(account_and_goals)
        self.accounts_name = list(self.accounts.keys())
        self.counter = 0
        self.state = state
        run_thread = threading.Thread(target=self.run(), args=())
        run_thread.daemon = True
        run_thread.start()

    def format_accounts(self, account_and_goals: List[AccountAndGoal]) -> dict:
        to_return = dict()
        for account_and_goal in account_and_goals:
            to_return[account_and_goal.get_name()] = account_and_goal
        return to_return

    def get_accounts_name(self):
        while True:
            account_name = self.accounts_name.pop(0)
            self.accounts_name.append(account_name)
            yield account_name

    def check_internet_status(self):
        status = self.state.get("status")
        prints = [
            "Wainting for internet connection",
            "Wainting for internet connection.",
            "Wainting for internet connection..",
            "Wainting for internet connection...",
        ]
        while status == "disconnected":
            to_print = prints.pop(0)
            print(to_print, end="\r")
            prints.append(to_print)
            time.sleep(2)
        if status == "reconnecting":
            for account in self.accounts.values():
                account.reconnect()
            self.state.set_state(key="status", value="running")

    def run(self):
        print("Fudeu ankama")
        for account_name in self.get_accounts_name():
            self.check_internet_status()
            self.set_account_turn(account_name=account_name)
            self.call_account_run_function(account_name=account_name)
            # PODE TRAVAR CASO NAO RETONE OU FINALIZE MAX TIME PARA RESOLVER
            while self.state.get("turn_of") != "free":
                time.sleep(0.2)

    def call_account_run_function(self, account_name: str):
        try:
            self.accounts[account_name].run_function()
        except JobError as e:
            print("DEU MERDA", e)
            input()
        except CharacterCriticalError as e:
            print("DEU MERDA ao  ^2", e)
            input()

    def set_account_turn(self, account_name: str):
        self.state.set_state(key="turn_of", value=account_name)
