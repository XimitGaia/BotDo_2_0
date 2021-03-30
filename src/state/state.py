import threading
import time

#Pause resume meche direto no state, o resolve queue tem que olhar state para ver se pausou


class State:

    def __init__(self, state: dict, debug: bool = False):
        self.debug = debug
        self.state = state
        self.is_bussy = False
        self.queue = list()
        self.temp_state_store = None
        resolve_queue_thread = threading.Thread(target=self.resolve_queue, args=())
        resolve_queue_thread.daemon = True
        resolve_queue_thread.start()

    def set_state(self, key, value):
        if self.debug:
            print(f'set_state -> value: {value}, key: {key}')
        self.queue.append({'value': value, 'key': key})

    def pause(self):
        self.temp_state_store = self.get('status')
        self._set_state(key='status', value='paused')

    def resume(self):
        self._set_state(key='status', value=self.temp_state_store)
        self.temp_state_store = None

    def set_thread_status(self, thread_name, running_or_paused):
        self.state['threads_status'][thread_name] = running_or_paused

    def get(self, key):
        return self.state[key]

    def resolve_queue(self):
        self.set_thread_status('resolve_queue_thread', 'runnning')
        while True:
            self.check_pause_command()
            # print(f'is_busy: {self.is_bussy}')
            if len(self.queue) > 0:
                to_exec = self.queue.pop(0)
                if self.debug:
                    print(f'to_exec -> {to_exec}')
                if not self.is_bussy:
                    self._set_state(key=to_exec['key'], value=to_exec['value'])
                else:
                    while True:
                        self.check_pause_command()
                        if not self.is_bussy:
                            self._set_state(key=to_exec['key'], value=to_exec['value'])
                            break
                        time.sleep(1)
            else:
                time.sleep(1)

    def check_pause_command(self):
        if self.get('status') == 'paused':
            self.set_thread_status('resolve_queue_thread', 'paused')
            while True:
                if self.get('status') != 'paused':
                    self.set_thread_status('resolve_queue_thread', 'runnning')
                    break
                print(self.get('threads_status'))
                time.sleep(1)

    def _set_state(self, key, value):
        self.state[str(key)] = value
        if value == 'battle':
            self.is_bussy = True
