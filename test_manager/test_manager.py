#!/usr/bin/env python3

###############################################################################
class Test_Manager:

    def __init__(self,bench):
        self.test_list=[]
        self.bench=bench

    def add_test_to_stack(self,test):
        self.test_list.append(test)
    
    def remove_test_from_stack(self,test):
        self.test_list.remove(test)

    def run_test_stack(self):
        for test in self.test_list:
            test.run()

