#!/usr/bin/env python3

import funcgen.fy3224s as fg;
import psu.owon_spm3051 as psu;
import oscilloscope.gw_instek_gds_806s as osc;
import time;

###############################################################################
if(0):
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
if(0):
    funcGen = fg.FeelTech('COM10')
    funcGen.debug_mode = True

    funcGen.open()

    print("Device ID:",funcGen.get_device_id())

    funcGen.set_waveform(fg.Waveform.square)
    funcGen.set_frequency(1010.11)
    funcGen.set_amplitude(1.1)
    funcGen.set_DC_offset(2.4)
    funcGen.set_duty_cycle(14.2)
    funcGen.set_pulse_width(1234,'ns') #not working

    funcGen.set_deputy_waveform(fg.Waveform.sine)
    funcGen.set_deputy_frequency(1010.12)
    funcGen.set_deputy_amplitude(1.2)
    funcGen.set_deputy_DC_offset(2.5)
    funcGen.set_deputy_duty_cycle(14.3)
    funcGen.set_deputy_wave_phase(123) 

    funcGen.set_sweep_time(51)
    funcGen.set_sweep_start_frequency(15.3)
    funcGen.set_sweep_stop_frequency(20.2) 
    funcGen.set_scan_mode('lin-sweep')
    funcGen.set_sweep_control('stop')
    funcGen.clear_internal_counter()
    funcGen.store_current_parameters(2)
    funcGen.load_current_parameters(2)
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

    oscilloscope.clear_event_registers()

    print("get oscilloscope settings:",oscilloscope.get_oscilloscope_settings())

    oscilloscope.reset_oscilloscope_settings()
    
    print("is operation completed?",oscilloscope.is_operation_complete())

    oscilloscope.perform_autoset()

    oscilloscope.run()

    oscilloscope.stop()

    oscilloscope.acquire_mode(osc.Acquire_Mode.average_mode)
    oscilloscope.acquire_average(osc.Acquire_Average.ave_4)
    oscilloscope.acquire_length(osc.Acquire_Length.len_1250)
    oscilloscope.acquire_memory(osc.Channel.ch1)
    oscilloscope.acquire_point(osc.Channel.ch1)
    oscilloscope.set_timebase_delay(00.1)
    oscilloscope.set_timebase_scale(osc.Time_Scale.ms_1)
    oscilloscope.set_trigger_mode(osc.Trigger_Mode.auto)
    oscilloscope.set_trigger_type(osc.Trigger_Type.delay)
    oscilloscope.set_trigger_source(osc.Trigger_Source.ch1)
    oscilloscope.set_trigger_couple(osc.Trigger_Coupling.AC)
    oscilloscope.set_trigger_level(2.1)
    oscilloscope.set_trigger_slope(osc.Trigger_Slope.falling_slope)
    oscilloscope.set_trigger_video_line(2.1)
    oscilloscope.set_trigger_video_polarity(osc.Trigger_Video_Polarity.negative)
    oscilloscope.enable_channel_invert(osc.Channel.ch1,1)
    oscilloscope.enable_channel_bw_limit(osc.Channel.ch1,1)
    oscilloscope.channel_coupling(osc.Channel.ch1,osc.Channel_Coupling.AC)
    oscilloscope.channel_math(osc.Channel.ch1,osc.Channel_Math.FFT)
    oscilloscope.channel_offset(osc.Channel.ch1,osc.Voltage_Scale.mV_1)
    oscilloscope.channel_probe(osc.Channel.ch1,osc.Channel_Probe.X_10)
    oscilloscope.channel_scale(1,osc.Voltage_Scale.mV_1)
    oscilloscope.measure_source(osc.Channel.ch1)
    oscilloscope.measure_fall()
    oscilloscope.measure_rise()
    oscilloscope.measure_negative_pulse()
    oscilloscope.measure_positive_pulse()
    oscilloscope.measure_pulse_width()
    oscilloscope.measure_frequency()
    oscilloscope.measure_period()
    oscilloscope.measure_voltage_amplitude()
    oscilloscope.measure_voltage_average()
    oscilloscope.measure_voltage_high()
    oscilloscope.measure_voltage_low()
    oscilloscope.measure_voltage_max()
    oscilloscope.measure_voltage_min()
    oscilloscope.measure_voltage_peak_to_peak()
    oscilloscope.measure_voltage_rms()

    oscilloscope.close()