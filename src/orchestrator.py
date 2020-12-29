# Autoloader
import sys
import os
import time
from pathlib import Path
path = Path(__file__).resolve()
sys.path.append(str(path.parents[0]))

from src.state.state import State
import threading


class Orchestrator:

    def __init__(self, accounts: dict, state: State):
        self.accounts_name = list(accounts.keys())
        self.accounts = accounts
        self.counter = 0
        self.state = state
        run_thread = threading.Thread(target=self.run(), args=())
        run_thread.daemon = True
        run_thread.start()

    def get_accounts_name(self):
        while True:
            account_name = self.accounts_name.pop(0)
            self.accounts_name.append(account_name)
            yield account_name

    def run(self):
        print('Fudeu ankama')
        for account_name in self.get_accounts_name():
            self.state.set_state(key='turn_off', value=account_name)
            self.accounts[account_name].run_function()
            # PODE TRAVAR CASO NAO RETONE OU FINALIZE MAX TIME PARA RESOLVER
            while self.state.get('turn_off') != 'free':
                time.sleep(0.2)
