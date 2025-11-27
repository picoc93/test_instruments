import json
from types import SimpleNamespace

class Test:

    def __init__(self, bench):
        self.bench=bench
        with open(self.id + '.json') as init_file:
            self = json.loads(init_file,object_hook=lambda d: SimpleNamespace(**d))

    def run(self):
        self.initialization()
        self.loop()
        self.termination()

    def initialization(self):
        return

    def loop(self):
        return

    def termination(self):
        #write report
        return

