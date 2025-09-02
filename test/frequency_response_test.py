#!/usr/bin/env python3

import instruments.awg.fy3224s as fg;
import instruments.psu.owon_spm3051 as psu;
import instruments.oscilloscope.gw_instek_gds_806s as osc;
import time;

###############################################################################

class Frequency_Response_Test():

    def __init__(self):
        self.power_supply=None
        self.function_generator=None
        self.oscilloscope=None
        
        power_supply_connect()
        function_generator_connect()
        oscilloscope_connect()

        power_supply_init()        
        function_generator_init()
        oscilloscope_init()

    def __del__(self):
        self.power_supply.close()
        self.function_generator.close()
        self.oscilloscope.close()

    def power_supply_connect(self):
        self.power_supply=psu.Owon('COM14')
        self.power_supply.open()

    def function_generator_connect(self):
        self.function_generator = fg.FeelTech('COM10')
        self.function_generator.open()

    def oscilloscope_connect(self):
        self.oscilloscope=osc.GWInstek('COM11')
        self.oscilloscope.open()

    def power_supply_init(self):
        print("Set Voltage Limit:",power_supply.set_voltage_limit(10))
        print("Set Current Limit:",power_supply.set_current_limit(1))
        print("Set Output:", power_supply.set_output(True))

    def function_generator_init(self):
        print("Set deputy waveform:",function_generator.set_deputy_waveform(fg.Waveform.sine))
        print("Set deputy frequency:",function_generator.set_deputy_frequency(1010.12))
        print("Set deputy amplitude:",function_generator.set_deputy_amplitude(1.2))
        print("Set deputy DC offset:",function_generator.set_deputy_DC_offset(2.5))
        print("Set deputy duty cycle:",function_generator.set_deputy_duty_cycle(14.3))
        print("Set deputy pulse width:",function_generator.set_deputy_wave_phase(123)) 

        print("Set sweep time:",function_generator.set_sweep_time(51))
        print("Set sweep start frequency:",function_generator.set_sweep_start_frequency(15.3))
        print("Set sweep stop frequency",function_generator.set_sweep_stop_frequency(20.2))
        print("Set scan mode:",function_generator.set_scan_mode('lin-sweep'))
        print("Set sweep control:",function_generator.set_sweep_control('stop'))

        print("Clear internal counter:",function_generator.clear_internal_counter())
        print("Store current parameter:",function_generator.store_current_parameters(2))
        print("Load current parameter:",function_generator.load_current_parameters(2))

        print("get frequency:",function_generator.get_frequency())
        print("get duty cycle:",function_generator.get_duty_cycle())
        print("get sweep time values:",function_generator.get_sweep_time_values())
        print("get external frequency:",function_generator.get_external_frequency())
        print("get external count:",function_generator.get_external_count())

    def oscilloscope_init(self):   
        print("Identity:",oscilloscope.read_identity())
        print("status enable register",oscilloscope.get_event_status_enable_register())
        print("status byte register",oscilloscope.get_status_byte_register())

        print("clear event register",oscilloscope.clear_event_registers())

        print("get oscilloscope settings:",oscilloscope.get_oscilloscope_settings())

        print("reset oscilloscope settings",oscilloscope.reset_oscilloscope_settings())

        print("is operation completed?",oscilloscope.is_operation_complete())

        print("oscilloscope perform autoset",oscilloscope.perform_autoset())

        print("oscilloscope run",oscilloscope.run())
        print("oscilloscope run",oscilloscope.stop())

        print("acquire mode:",oscilloscope.acquire_mode(osc.Acquire_Mode.average_mode))
        print("acquire average:",oscilloscope.acquire_average(osc.Acquire_Average.ave_4))
        print("acquire length:",oscilloscope.acquire_length(osc.Acquire_Length.len_1250))
        print("acquire memory:",oscilloscope.acquire_memory(osc.Channel.ch1))
        print("acquire point:",oscilloscope.acquire_point(osc.Channel.ch1))

        print("set timebase delay:",oscilloscope.set_timebase_delay(00.1))
        print("Set timebase scale:",oscilloscope.set_timebase_scale(osc.Time_Scale.ms_1))
        print("Set trigger mode:",oscilloscope.set_trigger_mode(osc.Trigger_Mode.auto))
        print("Set trigger type:",oscilloscope.set_trigger_type(osc.Trigger_Type.delay))
        print("Set trigger source:",oscilloscope.set_trigger_source(osc.Trigger_Source.ch1))
        print("Set trigger couple:",oscilloscope.set_trigger_couple(osc.Trigger_Coupling.AC))
        print("Set trigger level:",oscilloscope.set_trigger_level(2.1))
        print("Set trigger slope:",oscilloscope.set_trigger_slope(osc.Trigger_Slope.falling_slope))
        print("Set trigger video line:",oscilloscope.set_trigger_video_line(2.1))
        print("Set trigger video polarity:",oscilloscope.set_trigger_video_polarity(osc.Trigger_Video_Polarity.negative))
        print("Enable channel invert:",oscilloscope.enable_channel_invert(osc.Channel.ch1,1))
        print("Enable NW limit:",oscilloscope.enable_channel_bw_limit(osc.Channel.ch1,1))
        print("Channel coupling:",oscilloscope.channel_coupling(osc.Channel.ch1,osc.Channel_Coupling.AC))
        print("Channel math:",oscilloscope.channel_math(osc.Channel.ch1,osc.Channel_Math.FFT))
        print("Channel offset:",oscilloscope.channel_offset(osc.Channel.ch1,osc.Voltage_Scale.mV_1))
        print("Channel probe:",oscilloscope.channel_probe(osc.Channel.ch1,osc.Channel_Probe.X_10))
        print("Channel scale:",oscilloscope.channel_scale(1,osc.Voltage_Scale.mV_1))
        print("measure source:",oscilloscope.measure_source(osc.Channel.ch1))
        print("measure fall:",oscilloscope.measure_fall())
        print("measure rise:",oscilloscope.measure_rise())
        print("measure negative pulse:",oscilloscope.measure_negative_pulse())
        print("measure positive pulse:",oscilloscope.measure_positive_pulse())
        print("measure pulse width:",oscilloscope.measure_pulse_width())
        print("measure frequency:",oscilloscope.measure_frequency())
        print("measure period:",oscilloscope.measure_period())
        print("measure voltage amplitude:",oscilloscope.measure_voltage_amplitude())
        print("measure voltage average:",oscilloscope.measure_voltage_average())
        print("measure voltage high:",oscilloscope.measure_voltage_high())
        print("measure voltage low:",oscilloscope.measure_voltage_low())
        print("measure voltage max:",oscilloscope.measure_voltage_max())
        print("measure voltage min:",oscilloscope.measure_voltage_min())
        print("measure voltage peak to peak:",oscilloscope.measure_voltage_peak_to_peak())
        print("measure voltage rms:",oscilloscope.measure_voltage_rms())

    def run(self):

        print("Measured Voltage:", psu.measure_voltage())
        print("Measured Current:", psu.measure_current())
        print("Get Voltage:", psu.get_voltage())
        print("Get Current:", psu.get_current())
        print("Set Voltage:",psu.set_voltage(3))
        print("Set Current:",psu.set_current(2))


 