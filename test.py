#!/usr/bin/env python3

import awg.fy3224s as fg;
import psu.owon_spm3051 as psu;
import oscilloscope.gw_instek_gds_806s as osc;
import time;

###############################################################################
if(1):
    psu=psu.Owon('COM14')
    psu.open()
    print("Identity:", psu.read_identity())
    print("Measured Voltage:", psu.measure_voltage())
    print("Measured Current:", psu.measure_current())
    print("Get Voltage:", psu.get_voltage())
    print("Get Current:", psu.get_current())
    print("Get Voltage Limit:", psu.get_voltage_limit())
    print("Get Current Limit:", psu.get_current_limit())
    print("Is Output enabled:", psu.get_output())

    print("Set Voltage:",psu.set_voltage(3))
    print("Set Current:",psu.set_current(2))
    print("Set Voltage Limit:",psu.set_voltage_limit(30))
    print("Set Current Limit:",psu.set_current_limit(3))
    print("Set Output:", psu.set_output(True))

    psu.close()

###############################################################################
if(1):
    funcGen = fg.FeelTech('COM10')

    funcGen.open()

    print("Device ID:",funcGen.get_device_id())

    print("Set waveform:",funcGen.set_waveform(fg.Waveform.square))
    print("Set frequency:",funcGen.set_frequency(1010.11))
    print("Set amplitude:",funcGen.set_amplitude(1.1))
    print("Set DC offset:",funcGen.set_DC_offset(2.4))
    print("Set duty cycle:",funcGen.set_duty_cycle(14.2))
    print("Set pulse width:",funcGen.set_pulse_width(1234,'ns')) #not working

    print("Set deputy waveform:",funcGen.set_deputy_waveform(fg.Waveform.sine))
    print("Set deputy frequency:",funcGen.set_deputy_frequency(1010.12))
    print("Set deputy amplitude:",funcGen.set_deputy_amplitude(1.2))
    print("Set deputy DC offset:",funcGen.set_deputy_DC_offset(2.5))
    print("Set deputy duty cycle:",funcGen.set_deputy_duty_cycle(14.3))
    print("Set deputy pulse width:",funcGen.set_deputy_wave_phase(123)) 

    print("Set sweep time:",funcGen.set_sweep_time(51))
    print("Set sweep start frequency:",funcGen.set_sweep_start_frequency(15.3))
    print("Set sweep stop frequency",funcGen.set_sweep_stop_frequency(20.2))
    print("Set scan mode:",funcGen.set_scan_mode('lin-sweep'))
    print("Set sweep control:",funcGen.set_sweep_control('stop'))

    print("Clear internal counter:",funcGen.clear_internal_counter())
    print("Store current parameter:",funcGen.store_current_parameters(2))
    print("Load current parameter:",funcGen.load_current_parameters(2))

    print("get frequency:",funcGen.get_frequency())
    print("get duty cycle:",funcGen.get_duty_cycle())
    print("get sweep time values:",funcGen.get_sweep_time_values())
    print("get external frequency:",funcGen.get_external_frequency())
    print("get external count:",funcGen.get_external_count())

    funcGen.close()

###############################################################################

if(1):
    oscilloscope=osc.GWInstek('COM11')
    oscilloscope.open()

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

    oscilloscope.close()