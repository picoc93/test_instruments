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
oscilloscope.acquire_average(2)

#0→Record length is 500 1→Record length is 1250 2→Record length is 2500
#3→Record length is 5000 4→Record length is 12500 5→Record length is 25000
#6→Record length is 50000 7→Record length is 125000
oscilloscope.acquire_length(1)

#<X>→Specify the channel number (1|2)
oscilloscope.acquire_memory(1)

#<X>→Specify the channel number (1|2)
oscilloscope.acquire_point(1)

oscilloscope.set_timebase_delay(0.2)

#Sec/div	NR3
#1ns	1.00E-09
#2.5ns	2.50E-09
#5ns	5.00E-09
#10ns	1.00E-08
#25ns	2.50E-08
#50ns	5.00E-08
#100ns	1.00E-07
#250ns	2.50E-07
#500ns	5.00E-07
#1μs	1.00E-06
#2.5μs	2.50E-06
#5μs	5.00E-06
#10μs	1.00E-05
#25μs	2.50E-05
#50μs	5.00E-05
#100μs	1.00E-04
#250μs	2.50E-04
#500μs	5.00E-04
#1ms	1.00E-03
#2.5ms	2.50E-03
#5ms	5.00E-03
#10ms	1.00E-02
#25ms	2.50E-02
#50ms	5.00E-02
#100ms	1.00E-01
#250ms	2.50E-01
#500ms	5.00E-01
#1s	1
#2.5s	2.5
#5s	5
#10s	10

oscilloscope.set_timebase_scale(2) #to be reviewed

#0→Auto Level
#1→Auto
#2→Normal
#3→Single
oscilloscope.set_trigger_mode(0)

#0→Edge 
#1→Video 
#2→Pulse 
#3→Delay
oscilloscope.set_trigger_type(0)

#0→Channel 1 
#1→Channel 2 
#2→External trigger 
#3→AC line voltage
oscilloscope.set_trigger_source(0)

#0→AC 1→DC
oscilloscope.set_trigger_couple(0)
oscilloscope.set_trigger_level(2.1)

#0→Rising slope 1→Falling slope 
oscilloscope.set_trigger_slope(0)
oscilloscope.set_trigger_video_line(2.1)

#0→Positive-going sync pulses
#1→Negative-going sync pulses
oscilloscope.set_trigger_video_polarity(0)

#<X>→Specify the channel number (1|2) 
#0→Disable invert function 1→Enable invert function 
oscilloscope.enable_channel_invert(1,1)

#0→Disable bandwidth limit 1→Enable bandwidth limit
#<X>→Specify the channel number (1|2)
oscilloscope.enable_channel_bw_limit(1, 1)

#<X>→Specify the channel number (1|2)
#0→Place scope in AC coupling state 1→Place scope in DC coupling state
#2→Place scope in grounding state
oscilloscope.channel_coupling(1,0)

#<X>→Specify the channel number (1|2)
#0→Select the add operator 1→Select the subtract operator
#2→Select the FFT operation 3→Turn off math function
oscilloscope.channel_math(1,2)

#<X>→Specify the channel number (1|2)
#<NR3> is the desired offset value in volts. The range is dependent on the scale the probe attenuation factor. The offset ranges are following:7
#0.002->2mV
#0.005->2mV
#0.01->10mV
#0.02->20mV
#0.05->50mV
#0.1->100mV
#0.2->200mV 
#0.5->500mV
#1->1V
#2->2V
#5->5V
oscilloscope.channel_offset(1,2) #to be adjusted

#<X>→Specify the channel number (1|2)
#0→1X 1→10X 2→100X
oscilloscope.channel_probe(1,1)

#<X>→Specify the channel number (1|2)
#<NR3> is the desired gain value in volts per division. The range is 2mV/div to 5V/div (with 1X probe).
#0.002->2mV
#0.005->2mV
#0.01->10mV
#0.02->20mV
#0.05->50mV
#0.1->100mV
#0.2->200mV 
#0.5->500mV
#1->1V
#2->2V
#5->5V
oscilloscope.channel_scale(1,scale):

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