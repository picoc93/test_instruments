#!/usr/bin/env python3
import time

class Instrument_Commands_Test:

    def __init__(self, bench):
        #required instruments
        self.start_time=None
        self.stop_time=None
        self.bench=bench        
###############################################################################

    def run(self):
        self.start_time=time.time()
        self.test_initialization()
        self.test_loop()
        self.test_termination()
        self.stop_time=time.time()

    def test_initialization(self):
        return

    def test_loop(self):
        self.bench.power_supply.read_identity()
        self.bench.power_supply.measure_voltage()
        self.bench.power_supply.measure_current()
        self.bench.power_supply.get_voltage()
        self.bench.power_supply.get_current()
        self.bench.power_supply.get_voltage_limit()
        self.bench.power_supply.get_current_limit()
        self.bench.power_supply.get_output()
        self.bench.power_supply.set_voltage(3)
        self.bench.power_supply.set_current(2)
        self.bench.power_supply.set_voltage_limit(30)
        self.bench.power_supply.set_current_limit(3)
        self.bench.power_supply.psu.set_output(True)

        self.bench.function_generator.get_device_id()
        self.bench.function_generator.set_waveform(self.bench.function_generator.Waveform.square)
        self.bench.function_generator.set_frequency(1010.11)
        self.bench.function_generator.set_amplitude(1.1)
        self.bench.function_generator.set_DC_offset(2.4)
        self.bench.function_generator.set_duty_cycle(14.2)
        self.bench.function_generator.set_pulse_width(1234,'ns') #not working
        self.bench.function_generator.set_deputy_waveform(self.bench.function_generator.Waveform.sine)
        self.bench.function_generator.set_deputy_frequency(1010.12)
        self.bench.function_generator.set_deputy_amplitude(1.2)
        self.bench.function_generator.set_deputy_DC_offset(2.5)
        self.bench.function_generator.set_deputy_duty_cycle(14.3)
        self.bench.function_generator.set_deputy_wave_phase(123)
        self.bench.function_generator.set_sweep_time(51)
        self.bench.function_generator.set_sweep_start_frequency(15.3)
        self.bench.function_generator.set_sweep_stop_frequency(20.2)
        self.bench.function_generator.set_scan_mode('lin-sweep')
        self.bench.function_generator.set_sweep_control('stop')
        self.bench.function_generator.clear_internal_counter()
        self.bench.function_generator.store_current_parameters(2)
        self.bench.function_generator.load_current_parameters(2)
        self.bench.function_generator.get_frequency()
        self.bench.function_generator.get_duty_cycle()
        self.bench.function_generator.get_sweep_time_values()
        self.bench.function_generator.get_external_frequency()
        self.bench.function_generator.get_external_count()
        
        self.bench.oscilloscope.read_identity()
        self.bench.oscilloscope.get_event_status_enable_register()
        self.bench.oscilloscope.get_status_byte_register()
        self.bench.oscilloscope.clear_event_registers()
        self.bench.oscilloscope.get_oscilloscope_settings()
        self.bench.oscilloscope.reset_oscilloscope_settings()
        self.bench.oscilloscope.is_operation_complete()
        self.bench.oscilloscope.perform_autoset()
        self.bench.oscilloscope.run()
        self.bench.oscilloscope.stop()
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
        self.bench.oscilloscope.set_trigger_video_line(2.1)
        self.bench.oscilloscope.set_trigger_video_polarity(self.bench.oscilloscope.Trigger_Video_Polarity.negative)
        self.bench.oscilloscope.enable_channel_invert(self.bench.oscilloscope.Channel.ch1,1)
        self.bench.oscilloscope.enable_channel_bw_limit(self.bench.oscilloscope.Channel.ch1,1)
        self.bench.oscilloscope.channel_coupling(self.bench.oscilloscope.Channel.ch1,self.bench.oscilloscope.Channel_Coupling.AC)
        self.bench.oscilloscope.channel_math(self.bench.oscilloscope.Channel.ch1,self.bench.oscilloscope.Channel_Math.FFT)
        self.bench.oscilloscope.channel_offset(self.bench.oscilloscope.Channel.ch1,self.bench.oscilloscope.Voltage_Scale.mV_1)
        self.bench.oscilloscope.channel_probe(self.bench.oscilloscope.Channel.ch1,self.bench.oscilloscope.Channel_Probe.X_10)
        self.bench.oscilloscope.channel_scale(1,self.bench.oscilloscope.Voltage_Scale.mV_1)
        self.bench.oscilloscope.measure_source(self.bench.oscilloscope.Channel.ch1)
        self.bench.oscilloscope.measure_fall()
        self.bench.oscilloscope.measure_rise()
        self.bench.oscilloscope.measure_negative_pulse()
        self.bench.oscilloscope.measure_positive_pulse()
        self.bench.oscilloscope.measure_pulse_width()
        self.bench.oscilloscope.measure_frequency()
        self.bench.oscilloscope.measure_period()
        self.bench.oscilloscope.measure_voltage_amplitude()
        self.bench.oscilloscope.measure_voltage_average()
        self.bench.oscilloscope.measure_voltage_high()
        self.bench.oscilloscope.measure_voltage_low()
        self.bench.oscilloscope.measure_voltage_max()
        self.bench.oscilloscope.measure_voltage_min()
        self.bench.oscilloscope.measure_voltage_peak_to_peak()
        self.bench.oscilloscope.measure_voltage_rms()

