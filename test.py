#!/usr/bin/env python3

import funcgen.fy3224s as fg;
import psu.owon_spm3051 as psu;
import oscilloscope.gw_instek_gds_806s as osc;
import time;

###############################################################################

funcGen = fg.Generator('COM10')
funcGen.debug_mode = True

funcGen.get_device_id()

funcGen.set_waveform(fg.Waveform.square)
funcGen.set_frequency(1010.11)
funcGen.set_amplitude(1.1)
funcGen.set_DC_offset(2.4)
funcGen.set_duty_cycle(14.2)
funcGen.set_pulse_width(1234,'ns') #not working

#funcGen.set_deputy_waveform(fg.Waveform.sine)
#funcGen.set_deputy_frequency(1010.12)
#funcGen.set_deputy_amplitude(1.2)
#funcGen.set_deputy_DC_offset(2.5)
#funcGen.set_deputy_duty_cycle(14.3)
#funcGen.set_deputy_wave_phase(123) 

#funcGen.set_sweep_time(51)
#funcGen.set_sweep_start_frequency(15.3)
#funcGen.set_sweep_stop_frequency(20.2) 
#funcGen.set_scan_mode('lin-sweep')
#funcGen.set_sweep_control('stop')

#funcGen.clear_internal_counter()
#funcGen.store_current_parameters(2)
#funcGen.load_current_parameters(2)

#funcGen.get_frequency()
#funcGen.get_duty_cycle()
#funcGen.get_sweep_time_values()
#funcGen.get_external_frequency()
#funcGen.get_external_count()

funcGen.close()

###############################################################################

psu=psu.OwonPSU('COM13')
psu.open()
print("Identity:", psu.read_identity())
print("Measured Voltage:", psu.measure_voltage())
print("Measured Current:", psu.measure_current())
print("Get Voltage:", psu.get_voltage())
print("Get Current:", psu.get_current())
print("Get Voltage Limit:", psu.get_voltage_limit())
print("Get Current Limit:", psu.get_current_limit())

psu.set_voltage(3)
psu.set_current(2)
psu.set_voltage_limit(30)
psu.set_current_limit(3)

print("Output enabled:", psu.get_output())
psu.set_output(True)
psu.close()

###############################################################################

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

#0→Select the sample mode 
#1→Select the peak detection mode
#2→Select the average mode
oscilloscope.acquire_mode(1)

#1→Average number is 2 2→Average number is 4
#3→Average number is 8 4→Average number is 16
#5→Average number is 32 6→Average number is 64
#7→Average number is 128 8→Average number is 256
oscilloscope.acquire_average(number)

#0→Record length is 500 1→Record length is 1250 2→Record length is 2500
#3→Record length is 5000 4→Record length is 12500 5→Record length is 25000
#6→Record length is 50000 7→Record length is 125000
oscilloscope.acquire_length(number)

#<X>→Specify the channel number (1|2)
oscilloscope.acquire_memory(channel)

#<X>→Specify the channel number (1|2)
oscilloscope.acquire_point(channel)

oscilloscope.set_timebase_delay(delay)
oscilloscope.set_timebase_scale(scale)

#0→Auto Level
#1→Auto
#2→Normal
#3→Single
oscilloscope.set_trigger_mode(mode)
  
oscilloscope.set_trigger_type(trigger_type)
oscilloscope.set_trigger_source(source)

#0→AC 1→DC
oscilloscope.set_trigger_couple(couple)
oscilloscope.set_trigger_level(level)
oscilloscope.set_trigger_slope(slope)
oscilloscope.set_trigger_video_line(line)

#0→Positive-going sync pulses
#1→Negative-going sync pulses
oscilloscope.set_trigger_video_polarity(polarity)

#<X>→Specify the channel number (1|2) 
#0→Disable invert function 1→Enable invert function 
oscilloscope.enable_channel_invert(channel,invert)

#0→Disable bandwidth limit 1→Enable bandwidth limit
#<X>→Specify the channel number (1|2)
oscilloscope.enable_channel_bw_limit(channel, bw_limit)

#<X>→Specify the channel number (1|2)
#0→Place scope in AC coupling state 1→Place scope in DC coupling state
#2→Place scope in grounding state
oscilloscope.channel_coupling(channel,coupling)

#<X>→Specify the channel number (1|2)
#0→Select the add operator 1→Select the subtract operator
#2→Select the FFT operation 3→Turn off math function
oscilloscope.channel_math(channel,math)

#<X>→Specify the channel number (1|2)
#<NR3> is the desired offset value in volts. The range is dependent on the scale the probe attenuation factor. The offset ranges are following:
oscilloscope.channel_offset(channel,offset)

#<X>→Specify the channel number (1|2)
#0→1X 1→10X 2→100X
oscilloscope.channel_probe(channel,probe)

#<X>→Specify the channel number (1|2)
#<NR3> is the desired gain value in volts per division. The range is 2mV/div to 5V/div (with 1X probe).
oscilloscope.channel_scale(channel,scale):

#Select the measured channel (channel 1 or 2). The default setting of measured channel is channel one.
#1→Enable the measurement functions for channel 1
#2→Enable the measurement functions for channel 2
oscilloscope.measure_source(channel)
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