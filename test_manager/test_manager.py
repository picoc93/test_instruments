#!/usr/bin/env python3
import time
import json
import time

class Test_Manager: #run tests, collect measures, insert measures in DB

    def __init__(self,bench):
        self.bench=bench
        self.test_stack=[]

    def run_test_stack(self):
        self.test_manager_initialization()
        self.test_manager_loop()
        self.test_manager_termination()

    def test_manager_initialization(self):
        print('ciao')
        self.start_time=time.time()

        return

    def test_manager_loop(self):
        return

    def test_manager_termination(self):
        self.stop_time=time.time()


