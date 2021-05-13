import threading
import time

#Pause resume meche direto no state, o resolve queue tem que olhar state para ver se pausou


class State:

    def __init__(self, state: dict, debug: bool = False):
        self.debug = debug
        self.state = state
        self.queue = list()
        self.temp_status_store = None
        self.priority_status = {
            'battle': ['disconnected', 'reconnecting', 'running'],
            'disconnected': ['reconnecting'],
            'reconnecting': ['running', 'disconnected'],
            'running': ['battle', 'disconnected', 'reconnecting']
        }
        resolve_queue_thread = threading.Thread(target=self.resolve_queue, args=())
        resolve_queue_thread.daemon = True
        resolve_queue_thread.start()

    def set_state(self, key, value):
        self.queue.append({'value': value, 'key': key})

    def set_thread_status(self, thread_name, status):
        self.state['threads_status'][thread_name] = status

    def pause(self):
        self.temp_state_store.update({'status_value': self.get('status'), 'is_busy': False})
        self._set_state(key='status', value='paused')

    def resume(self):
        self._set_state(key='status', value=self.temp_state_store.get('status_value'))
        self.temp_state_store.update({'status_value': None , 'is_busy': False})

    def get(self, key):
        return self.state[key]

    def resolve_queue(self):
        self.set_thread_status('resolve_queue_thread', 'runnning')
        while True:
            self.check_pause_command(thread_name='resolve_queue_thread')
            if len(self.queue) > 0:
                to_exec = self.queue.pop(0)
                self._set_state(key=to_exec['key'], value=to_exec['value'])
            else:
                time.sleep(1)

    def check_pause_command(self, thread_name):
        status = self.get('status')
        if self.is_pause_status(status=status, thread_name=thread_name):
            self.set_thread_status(thread_name, 'paused')
            while True:
                if not self.is_pause_status(status=status, thread_name=thread_name):
                    self.set_thread_status(thread_name, 'runnning')
                    break
                time.sleep(1)

    def is_pause_status(self, status, thread_name):
        if status == 'paused':
            return True
        if status == 'reconnecting' or status == 'disconnected':
            if thread_name == 'internet_observer_thread':
                return False
            return True

    def _set_state(self, key, value):
        if str(key) == 'status':
            if value not in self.priority_status.get(self.get('status')):
                return
        self.state[str(key)] = value

