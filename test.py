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

oscilloscope.close()