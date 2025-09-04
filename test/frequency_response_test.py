#!/usr/bin/env python3

import time

class Frequency_Response_Test:

    def __init__(self, bench):
        #required instruments
        self.start_time=None
        self.stop_time=None
        self.bench=bench        

    def run(self):
        self.start_time=time.time()
        self.test_initialization()
        self.test_loop()
        self.test_termination()
        self.stop_time=time.time()

    def test_initialization(self):
        self.power_supply_init()
        self.function_generator_init()
        self.oscilloscope_init()

    def power_supply_init(self):
        self.bench.power_supply.set_voltage_limit(10)
        self.bench.power_supply.set_current_limit(1)
        self.bench.power_supply.set_output(True)

    def function_generator_init(self):
        self.bench.function_generator.clear_internal_counter()
        self.bench.function_generator.set_deputy_waveform(fg.Waveform.sine)
        self.bench.function_generator.set_deputy_frequency(1010.12)
        self.bench.function_generator.set_deputy_amplitude(1.2)
        self.bench.function_generator.set_deputy_DC_offset(2.5)
        self.bench.function_generator.set_deputy_duty_cycle(14.3)
        self.bench.function_generator.set_deputy_wave_phase(123)

        self.bench.function_generator.set_sweep_time(51)
        self.bench.function_generator.set_sweep_start_frequency(15.3)
        self.bench.function_generator.set_sweep_stop_frequency(20.2)
        self.bench.function_generator.set_scan_mode('lin-sweep')

    def oscilloscope_init(self):   
        self.bench.oscilloscope.clear_event_registers()
        self.bench.oscilloscope.reset_oscilloscope_settings()
        self.bench.oscilloscope.perform_autoset()

        self.bench.oscilloscope.acquire_mode(self.bench.oscilloscope.Acquire_Mode.average_mode)
        self.bench.oscilloscope.acquire_average(self.bench.oscilloscope.Acquire_Average.ave_4)
        self.bench.oscilloscope.acquire_length(self.bench.oscilloscope.Acquire_Length.len_1250)
        self.bench.oscilloscope.acquire_memory(self.bench.oscilloscope.Channel.ch1)
        self.bench.oscilloscope.acquire_point(self.bench.oscilloscope.Channel.ch1)

        self.bench.oscilloscope.set_timebase_delay(00.1)
        self.bench.oscilloscope.set_timebase_scale(self.bench.oscilloscope.Time_Scale.ms_1)

        self.bench.oscilloscope.set_trigger_mode(self.bench.oscilloscope.Trigger_Mode.auto)
        self.bench.oscilloscope.set_trigger_type(self.bench.oscilloscope.Trigger_Type.delay)
        self.bench.oscilloscope.set_trigger_source(self.bench.oscilloscope.Trigger_Source.ch1)
        self.bench.oscilloscope.set_trigger_couple(self.bench.oscilloscope.Trigger_Coupling.AC)
        self.bench.oscilloscope.set_trigger_level(2.1)
        self.bench.oscilloscope.set_trigger_slope(self.bench.oscilloscope.Trigger_Slope.falling_slope)

        self.bench.oscilloscope.channel_coupling(self.bench.oscilloscope.Channel.ch1,self.bench.oscilloscope.Channel_Coupling.AC)
        self.bench.oscilloscope.channel_math(self.bench.oscilloscope.Channel.ch1,self.bench.oscilloscope.Channel_Math.FFT)
        self.bench.oscilloscope.channel_offset(self.bench.oscilloscope.Channel.ch1,self.bench.oscilloscope.Voltage_Scale.mV_1)
        self.bench.oscilloscope.channel_probe(self.bench.oscilloscope.Channel.ch1,self.bench.oscilloscope.Channel_Probe.X_10)
        self.bench.oscilloscope.channel_scale(1,self.bench.oscilloscope.Voltage_Scale.mV_1)
        self.bench.oscilloscope.measure_source(self.bench.oscilloscope.Channel.ch1)

    def test_loop(self):
        self.bench.power_supply.set_voltage(3)
        self.bench.power_supply.set_current(2)
        self.bench.power_supply.measure_voltage()
        self.bench.power_supply.measure_current()
        self.bench.power_supply.get_voltage()
        self.bench.power_supply.get_current()
        self.bench.function_generator.get_frequency()
        self.bench.function_generator.get_duty_cycle()
        self.bench.function_generator.get_sweep_time_values()
        self.bench.function_generator.get_external_frequency()
        self.bench.function_generator.get_external_count()
        self.bench.function_generator.set_sweep_control('stop')
        self.bench.oscilloscope.run()
        self.bench.oscilloscope.measure_voltage_amplitude()
        self.bench.oscilloscope.measure_voltage_average()
        self.bench.oscilloscope.measure_voltage_high()
        self.bench.oscilloscope.measure_voltage_low()
        self.bench.oscilloscope.measure_voltage_max()
        self.bench.oscilloscope.measure_voltage_min()
        self.bench.oscilloscope.measure_voltage_peak_to_peak()
        self.bench.oscilloscope.measure_voltage_rms()

        self.bench.oscilloscope.stop()

    def test_termination(self):
        return
    
