import json

class Test:

    def __init__(self, test_id, bench):
        self.id=test_id
        self.bench=bench

    def run(self):
        self.initialization()
        self.loop()
        self.termination()

    def initialization(self):
        with open(self.id + '.json') as f:
            d = json.load(f)
            print(d)
        return

    def loop(self):
        return

    def termination(self):
        #write report
        return

