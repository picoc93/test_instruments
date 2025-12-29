import instrument
import json

class Bench:
    def __init__(self, config_path):
        self.config_path = config_path
        self.active_bench = {}


    def load_bench(self):
        with open(self.config_path, 'r') as f:
            data = json.load(f)

        for item in data['instruments']:
            itype = item['type']
            brand = item['brand']
            res_id = item['resource_id']

            # Use the correct factory to build the instrument
            factory = self.factories.get(itype)
            if factory:
                # We store it in a dict for easy access, e.g., self.active_bench['psu']
                self.active_bench[itype] = factory.create_instrument(brand, res_id)
                print(f"Initialized {brand} {itype} at {res_id}")

    def get_instrument(self, itype) -> Instrument:
        return self.active_bench.get(itype)