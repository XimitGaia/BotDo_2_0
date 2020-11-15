import threading
import time


class State:
    def __init__(self, state: dict, debug: bool = False):
        self.debug = debug
        self.state = state
        self.is_bussy = False
        self.queue = list()
        thread = threading.Thread(target = self.resolve_queue, args=())
        thread.daemon = True
        thread.start()

    def set_state(self, key, value):
        if self.debug:
            print(f'set_state -> value: {value}, key: {key}')
        self.queue.insert(0, {'value': value, 'key': key})

    def get(self, key):
        return self.state[key]
    
    def resolve_queue(self):
        while True:
            print(self.is_bussy)
            if len(self.queue) > 0:
                to_exec = self.queue.pop()
                if self.debug:
                    print(f'to_exec -> {to_exec}')
                if not self.is_bussy:
                    self._set_state(key=to_exec['key'],value=to_exec['value'])
                else:
                    while True:
                        if not self.is_bussy:        
                            self._set_state(key=to_exec['key'],value=to_exec['value'])
                            break
                        time.sleep(1)
            else:
                time.sleep(1)
    
    def _set_state(self, key, value):
        self.state[str(key)] = value
        if value == 'battle':
            self.is_bussy = True
