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
class Generator:
    def __init__(self, device = 'COM10'):
        self._debug_mode = False
        
        self._serial = serial.Serial(device, 9600, timeout=1)
        self._serialIO = io.TextIOWrapper(io.BufferedRWPair(self._serial, self._serial), newline='')

    @property
    def debug_mode(self):
        return self._debug_mode

    @debug_mode.setter
    def debug_mode(self, value):
        self._debug_mode = value

    def is_open(self):
        return hasattr(self, '_serial') and self._serial is not None

    def close(self):
        self._serial.close()
        del self._serialIO
        del self._serial

    def __del__(self):
        if self.is_open():
            self.close()
    
    def write(self, data):
        if self._debug_mode:
            print('[send] ' + data.rstrip())
        self._serialIO.write(data)
        self._serialIO.flush()
    
    def writeCmd(self, cmd):
        self.write(cmd + '\r'+'\n')
        time.sleep(0.1)
    
    def readResult(self):
        result = self._serialIO.readline().rstrip()
        
        if self._debug_mode:
            print('[recv] ' + result)
        
        return result
    
    ###########################################################################
    
    def get_device_id(self):
        self.writeCmd('a')
        return self.readResult()

    def set_waveform(self,waveform):
        self.writeCmd(f'bw{waveform:1}')
        return self.readResult()

    def set_frequency(self,freqInHz):
        freq=freqInHz*100
        self.writeCmd(f'bf{freq:>9}')
        return self.readResult()

    def set_amplitude(self,ampl):
        self.writeCmd(f'ba{ampl:4.1f}')
        return self.readResult()

    def set_DC_offset(self,offset):
        self.writeCmd(f'bo{offset:5.1f}')
        return self.readResult()

    def set_duty_cycle(self,duty_cycle):
        self.writeCmd(f'bd{duty_cycle:>2}')
        return self.readResult()

    def set_pulse_width(self,pulse_width,time_unit):
        self.writeCmd(f'bu{pulse_width:4}{time_unit}')
        return self.readResult()

    def set_sweep_time(self,sweep_time):
        self.writeCmd(f'bt{sweep_time:>2}')
        return self.readResult()

    def set_sweep_start_frequency(self,freq):
        self.writeCmd(f'bb{freq:>9}')
        return self.readResult()

    def set_sweep_stop_frequency(self,freq):
        self.writeCmd(f'be{freq:>9}')
        return self.readResult()

        #Set the sweep scan mode
    def set_scan_mode(self,mode):
        self.writeCmd(f'bm{mode:1}')
        return self.readResult()

    def start_sweep(self,ctrl):
        self.writeCmd(f'br{ctrl:1}')
        return self.readResult()

    def clear_internal_counter(self):
        self.writeCmd(f'bc')
        return self.readResult()     

    # store parameters (frequency, duty cycle, waveform) to a storage Position (0-9)
    def store_current_parameters(self,pos):
        self.writeCmd(f'bs{pos:1}')
        return self.readResult()

    # load parameters (frequency, duty cycle, waveform) to a storage Position (0-9)
    def load_current_parameters(self,pos):
        self.writeCmd(f'bl{pos:1}')
        return self.readResult()

    # read current frequency value
    def get_frequency(self):
        self.writeCmd('cf')
        return self.readResult()

    # read current external frequency measurement
    def get_external_frequency(self):
        self.writeCmd('ce')
        return self.readResult()

    # read current external count
    def get_external_count(self):
        self.writeCmd('cc')
        return self.readResult()

    # read currently set duty cycle
    def get_duty_cycle(self):
        self.writeCmd('cd')
        return self.readResult()

    # read current sweep time value
    def get_sweep_time_values(self):
        self.writeCmd('ct')
        return self.readResult()

