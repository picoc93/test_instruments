#!/usr/bin/env python3

import time
import instrument
import bench

###############################################################################
class Test_Manager:

    def __init__(self,bench_id):
        self.test_list=[]
        self.bench=bench.Bench(bench_id)

    def connect_instruments(self):
        self.bench.connect_psu ('COM11')
        self.bench.connect_function_generator('COM10')
        self.bench.function_generator('COM14')

    def fill_test_stack(self):
        return

    def run_test_stack(self):
        return
