#!/usr/bin/env python3
import bench
import test_manager
import test

###############################################################################
def main():
    test_bench=bench.Bench('home')

    test_bench.connect_oscilloscope('COM11')
    test_bench.connect_function_generator('COM21')
    test_bench.connect_power_supply('COM22')

    test_handler=test_manager.Test_Manager(test_bench)
    test_handler.set_voltage_list([3.8])
    test_handler.add_test_to_stack(test.Instrument_Commands_Test(test_bench))
    test_handler.add_test_to_stack(test.Frequency_Response_Test(test_bench))

    test_handler.run_test_stack()

if __name__ == "__main__":
    main()