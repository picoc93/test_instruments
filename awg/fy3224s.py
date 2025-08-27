#!/usr/bin/env python3

import serial
import io
from enum import IntEnum
import time;

###############################################################################

class Waveform(IntEnum):
    sine = 0
    square = 1
    pulse = 2
    triangular=3
    sawtooth=4
    fall_sawtooth_wave=5
    dc=6
    pre1=7
    pre2=8
    pre3=9
    pre4=10
    pre5=11
    pre6=12
    pre7=13
    pre8=14
    pre9=15
    pre10=16
    arb1 = 17
    arb2 = 18
    arb3 = 19
    arb4 = 20

###############################################################################
class FeelTech:

    def __init__(self, port,cmd_timeout=0.5):
        self.ser = None
        self.port=port
        self.timeout=cmd_timeout
        #self._serialIO = io.TextIOWrapper(io.BufferedRWPair(self._serial, self._serial), newline='')

    def __del__(self):
        if self.is_open():
            self.close()

    def open(self):
        self.ser= serial.Serial(self.port, 9600, timeout=1)

    def is_open(self):
        return hasattr(self, 'ser') and self.ser is not None

    def close(self):
        self.ser.close()
    
    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()
    
    def writeCmd(self, command):
        if not self.is_open():
            raise Exception("Connection is not open!")
        
        self.ser.write(bytes(command, 'utf-8') + b"\n")
        ret = self.ser.readline().decode('utf-8')
        
        #if not ret.endswith("\n"):
        #    raise Exception(f"Wrong command ending: '{command}'!")
        
        return ret[:-2]

    def writeSilentCmd(self, command):
        if not self.is_open():
            raise Exception("Connection is not open!")
        
        self.ser.write(bytes(command, 'utf-8') + b"\n")
        ret = self.ser.readline().decode('utf-8')
        
        if ret[:-2] == "ERR":
            raise Exception(f"Error while executing command: '{command}'")
    
    def reset_serial_buffer(self):
        if not self.is_open():
            raise Exception("Connection is not open!")
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()
    
    ###########################################################################
    
    def get_device_id(self):
        return self.writeCmd('a')

    def set_waveform(self,waveform):
        return self.writeSilentCmd(f'bw{waveform:1}')
        

    def set_frequency(self,freqInHz):
        freq=int(freqInHz*100)
        return self.writeSilentCmd(f'bf{freq:09d}')

    def set_amplitude(self,ampl):
        return self.writeSilentCmd(f'ba{ampl:2.1f}')

    def set_DC_offset(self,offset):
        return self.writeSilentCmd(f'bo{offset:3.1f}')


    def set_duty_cycle(self,duty_cycle):
        duty=duty_cycle*10
        return self.writeSilentCmd(f'bd{duty:3}')

    def set_pulse_width(self,pulse_width,time_unit):
        pw=int(pulse_width)*1000
        return self.writeSilentCmd(f'bu{pw:010d}{time_unit}')

    def set_sweep_time(self,sweep_time):
        return self.writeSilentCmd(f'bt{sweep_time:>2}')

    def set_sweep_start_frequency(self,freqInHz):
        freq=int(freqInHz*100)
        return self.writeSilentCmd(f'bb{freq:09d}')

    def set_sweep_stop_frequency(self,freqInHz):
        freq=int(freqInHz*100)
        return self.writeSilentCmd(f'be{freq:09d}')
        
        #Set the sweep scan mode
    def set_scan_mode(self,sweep_mode):
        if(sweep_mode == 'lin-sweep'):
            mode=0
        elif(sweep_mode == 'log-sweep'):
            mode=1
        else:
            mode=0
        return self.writeSilentCmd(f'bm{mode:1}')

    def set_sweep_control(self,sweep_control):
        if(sweep_control == 'stop'):
            ctrl=0
        elif(sweep_control == 'start'):
            ctrl=1
        else:
            ctrl=0
        return self.writeSilentCmd(f'br{ctrl:1}')
        
    def clear_internal_counter(self):
        return self.writeSilentCmd(f'bc')

    # store parameters (frequency, duty cycle, waveform) to a storage Position (0-9)
    def store_current_parameters(self,pos):
        return self.writeSilentCmd(f'bs{pos:1}')

    # load parameters (frequency, duty cycle, waveform) to a storage Position (0-9)
    def load_current_parameters(self,pos):
        return self.writeSilentCmd(f'bl{pos:1}')

    # read current frequency value
    def get_frequency(self):
        return self.writeCmd('cf')

    # read current external frequency measurement
    def get_external_frequency(self):
        return self.writeCmd('ce')

    # read current external count
    def get_external_count(self):
        return self.writeCmd('cc')

    # read currently set duty cycle
    def get_duty_cycle(self):
        return self.writeCmd('cd')

    # read current sweep time value
    def get_sweep_time_values(self):
        return self.writeCmd('ct')

    def set_deputy_waveform(self,waveform):
        return self.writeSilentCmd(f'dw{waveform:1}')

    def set_deputy_frequency(self,freqInHz):
        freq=int(freqInHz*100)
        return self.writeSilentCmd(f'df{freq:09d}')

    def set_deputy_amplitude(self,ampl):
        return self.writeSilentCmd(f'da{ampl:2.1f}')
        
    def set_deputy_DC_offset(self,offset):
        return self.writeSilentCmd(f'do{offset:3.1f}')

    def set_deputy_wave_phase(self,phase):
        return self.writeSilentCmd(f'dp{phase:3}')

    def set_deputy_duty_cycle(self,duty_cycle):
        duty=duty_cycle*10
        return self.writeSilentCmd(f'dd{duty:3}')