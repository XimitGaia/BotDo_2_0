import time



class Resolver:


    def __init__(self,state):
        self.state = state
        self.run()


    def run(self):
        while True:
            print(self.state.state['status'])