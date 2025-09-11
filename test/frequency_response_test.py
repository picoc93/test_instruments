#!/usr/bin/env python3
import instrument

class Frequency_Response_Test:

    def __init__(self, bench, frequency_array):
        self.id="Frequency Response Test"
        self.bench=bench
        self.frequency_array=frequency_array
        self.voltage_array=[]

    def run(self):
        self.test_initialization()
        self.test_loop()
        self.test_termination()

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
        self.bench.function_generator.set_deputy_waveform(instrument.awg.Waveform.sine)
        self.bench.function_generator.set_deputy_DC_offset(0)
        self.bench.function_generator.set_deputy_wave_phase(0)

        #self.bench.function_generator.set_sweep_time(180)
        #self.bench.function_generator.set_sweep_start_frequency(20)
        #self.bench.function_generator.set_sweep_stop_frequency(20000)
        #self.bench.function_generator.set_scan_mode(instrument.awg.Scan_Mode.linear)

    def oscilloscope_init(self):   
        self.bench.oscilloscope.clear_event_registers()
        self.bench.oscilloscope.reset_oscilloscope_settings()
        self.bench.oscilloscope.perform_autoset()

        self.bench.oscilloscope.acquire_mode(instrument.oscilloscope.Acquire_Mode.average_mode)
        self.bench.oscilloscope.acquire_average(instrument.oscilloscope.Acquire_Average.ave_4)
        self.bench.oscilloscope.acquire_length(instrument.oscilloscope.Acquire_Length.len_1250)
  
        self.bench.oscilloscope.set_timebase_delay(0.0)
        self.bench.oscilloscope.set_timebase_scale(instrument.oscilloscope.Time_Scale.ms_1)

        self.bench.oscilloscope.set_trigger_mode(instrument.oscilloscope.Trigger_Mode.auto)
        self.bench.oscilloscope.set_trigger_source(instrument.oscilloscope.Trigger_Source.ch1)
        self.bench.oscilloscope.set_trigger_couple(instrument.oscilloscope.Trigger_Coupling.AC)
        self.bench.oscilloscope.set_trigger_level(0)
        self.bench.oscilloscope.set_trigger_slope(instrument.oscilloscope.Trigger_Slope.falling_slope)

        self.bench.oscilloscope.channel_coupling(instrument.oscilloscope.Channel.ch1,instrument.oscilloscope.Channel_Coupling.AC)
        self.bench.oscilloscope.channel_math(instrument.oscilloscope.Channel.ch1,instrument.oscilloscope.Channel_Math.FFT)
        self.bench.oscilloscope.channel_offset(instrument.oscilloscope.Channel.ch1,instrument.oscilloscope.Voltage_Scale.mV_1)
        self.bench.oscilloscope.channel_probe(instrument.oscilloscope.Channel.ch1,instrument.oscilloscope.Channel_Probe.X_10)
        self.bench.oscilloscope.channel_scale(1,instrument.oscilloscope.Voltage_Scale.mV_1)
        
        self.bench.oscilloscope.measure_source(instrument.oscilloscope.Channel.ch1)

    def test_loop(self):

        for frequency in self.frequency_array:

            self.bench.function_generator.set_deputy_frequency(frequency)
            self.bench.function_generator.set_deputy_amplitude(1.0)

            self.bench.oscilloscope.run()
            self.bench.oscilloscope.measure_voltage_amplitude()
            self.bench.oscilloscope.measure_voltage_average()
            self.bench.oscilloscope.measure_voltage_rms()
            self.bench.oscilloscope.stop()

    def test_termination(self):
        return
  
        