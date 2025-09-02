#!/usr/bin/env python3

import time
import bench.Bench

###############################################################################
class Frequency_Response_Test:

    def test_initialize():
        power_supply_init()
        function_generator_init()
        oscilloscope_init()


    def power_supply_init():
        self.power_supply.set_voltage_limit(10)
        self.power_supply.set_current_limit(1)
        self.power_supply.set_output(True)

    def function_generator_init(self):
        self.function_generator.clear_internal_counter()
        self.function_generator.set_deputy_waveform(fg.Waveform.sine)
        self.function_generator.set_deputy_frequency(1010.12)
        self.function_generator.set_deputy_amplitude(1.2)
        self.function_generator.set_deputy_DC_offset(2.5)
        self.function_generator.set_deputy_duty_cycle(14.3)
        self.function_generator.set_deputy_wave_phase(123)

        self.function_generator.set_sweep_time(51)
        self.function_generator.set_sweep_start_frequency(15.3)
        self.function_generator.set_sweep_stop_frequency(20.2)
        self.function_generator.set_scan_mode('lin-sweep')

    def oscilloscope_init(self):   
        self.oscilloscope.clear_event_registers()
        self.oscilloscope.reset_oscilloscope_settings()
        self.oscilloscope.perform_autoset()

        self.oscilloscope.acquire_mode(osc.Acquire_Mode.average_mode)
        self.oscilloscope.acquire_average(osc.Acquire_Average.ave_4)
        self.oscilloscope.acquire_length(osc.Acquire_Length.len_1250)
        self.oscilloscope.acquire_memory(osc.Channel.ch1)
        self.oscilloscope.acquire_point(osc.Channel.ch1)

        self.oscilloscope.set_timebase_delay(00.1)
        self.oscilloscope.set_timebase_scale(osc.Time_Scale.ms_1)

        self.oscilloscope.set_trigger_mode(osc.Trigger_Mode.auto)
        self.oscilloscope.set_trigger_type(osc.Trigger_Type.delay)
        self.oscilloscope.set_trigger_source(osc.Trigger_Source.ch1)
        self.oscilloscope.set_trigger_couple(osc.Trigger_Coupling.AC)
        self.oscilloscope.set_trigger_level(2.1)
        self.oscilloscope.set_trigger_slope(osc.Trigger_Slope.falling_slope)

        self.oscilloscope.channel_coupling(osc.Channel.ch1,osc.Channel_Coupling.AC)
        self.oscilloscope.channel_math(osc.Channel.ch1,osc.Channel_Math.FFT)
        self.oscilloscope.channel_offset(osc.Channel.ch1,osc.Voltage_Scale.mV_1)
        self.oscilloscope.channel_probe(osc.Channel.ch1,osc.Channel_Probe.X_10)
        self.oscilloscope.channel_scale(1,osc.Voltage_Scale.mV_1)
        self.oscilloscope.measure_source(osc.Channel.ch1)

    def run(self):
        self.start_time=time.time()

        self.power_supply.set_voltage(3)
        self.power_supply.set_current(2)

        self.power_supply.measure_voltage()
        self.power_supply.measure_current()
        self.power_supply.get_voltage()
        self.power_supply.get_current()

        self.function_generator.get_frequency()
        self.function_generator.get_duty_cycle()
        self.function_generator.get_sweep_time_values()
        self.function_generator.get_external_frequency()
        self.function_generator.get_external_count()
        self.function_generator.set_sweep_control('stop')

        self.oscilloscope.run()

        self.oscilloscope.measure_voltage_amplitude()
        self.oscilloscope.measure_voltage_average()
        self.oscilloscope.measure_voltage_high()
        self.oscilloscope.measure_voltage_low()
        self.oscilloscope.measure_voltage_max()
        self.oscilloscope.measure_voltage_min()
        self.oscilloscope.measure_voltage_peak_to_peak()
        self.oscilloscope.measure_voltage_rms()
        
        self.oscilloscope.stop()

        self.stop_time=time.time()