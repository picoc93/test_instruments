#!/usr/bin/env python3

import time

class Test_Manager: #run tests, collect measures, insert measures in DB

    def __init__(self,bench):
        self.bench=bench
        self.voltage_list=[]
        self.test_list=[]

    def add_test_to_stack(self,test):
        self.test_list.append(test)
    
    def remove_test_from_stack(self,test):
        self.test_list.remove(test)

    def add_external_voltage_to_stack(self,voltage):
        self.voltage_list.append(voltage)
    
    def remove_external_voltage_to_stack(self,voltage):
        self.voltage_list.remove(voltage)

    def run_test_stack(self):
        if self.test_list:
            for test in self.test_list:
                start_time=time.start()
                test.run()
                stop_time=time.stop()

    def run_test_stack_voltage_loop(self):
        if self.voltage_list:
            for voltage in self.voltage_list:
                self.bench.power_supply.set_voltage(voltage)
                self.run_test_stack()


