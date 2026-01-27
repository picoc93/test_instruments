import instrument
import json

class Bench:
    def __init__(self, config_path):
        self.config_path = config_path
        self.active_bench = {}


    def load_bench(self):
        with open(self.config_path, 'r') as f:
            data = json.load(f)

