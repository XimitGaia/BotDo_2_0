import threading
import time


class State:
    def __init__(self):
        self.state = dict({
            'status': '',
            'is_loged': False,
            'resources': [],
            'characters': None
            })
        self.is_bussy = False
        self.queue = list()
        thread = threading.Thread(target = self.resolve_queue, args=())
        thread.daemon = True
        thread.start()

    def set_state(self, key, value):
        self.queue.insert(0, {'value': value, 'key': key})

    def get(self, key):
        return self.state[key]
    
    def resolve_queue(self):
        while True:
            if len(self.queue) > 0:
                to_exec = self.queue.pop()
                if not self.is_bussy:
                    self.state[to_exec['key']] = to_exec['value']
                else:
                    while True:
                        if not self.is_bussy:
                            self.state[to_exec['key']] = to_exec['value']
                            break
            else:
                time.sleep(1)