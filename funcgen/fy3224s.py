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
        
        if not ret.endswith("\n"):
            raise Exception(f"Wrong command ending: '{command}'!")
        
        return ret[:-2]
    
    def reset_serial_buffer(self):
        if not self.is_open():
            raise Exception("Connection is not open!")
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

    
    ###########################################################################
    
    def get_device_id(self):
        self.writeCmd('a')
        return self.readResult()

    def set_waveform(self,waveform):
        self.writeCmd(f'bw{waveform:1}')
        return

    def set_frequency(self,freqInHz):
        freq=int(freqInHz*100)
        self.writeCmd(f'bf{freq:09d}')
        return

    def set_amplitude(self,ampl):
        self.writeCmd(f'ba{ampl:2.1f}')
        return

    def set_DC_offset(self,offset):
        self.writeCmd(f'bo{offset:3.1f}')
        return

    def set_duty_cycle(self,duty_cycle):
        duty=duty_cycle*10
        self.writeCmd(f'bd{duty:3}')
        return

    def set_pulse_width(self,pulse_width,time_unit):
        pw=int(pulse_width)*1000
        self.writeCmd(f'bu{pw:010d}{time_unit}')
        return

    def set_sweep_time(self,sweep_time):
        self.writeCmd(f'bt{sweep_time:>2}')
        return

    def set_sweep_start_frequency(self,freqInHz):
        freq=int(freqInHz*100)
        self.writeCmd(f'bb{freq:09d}')
        return

    def set_sweep_stop_frequency(self,freqInHz):
        freq=int(freqInHz*100)
        self.writeCmd(f'be{freq:09d}')
        return

        #Set the sweep scan mode
    def set_scan_mode(self,sweep_mode):
        if(sweep_mode == 'lin-sweep'):
            mode=0
        elif(sweep_mode == 'log-sweep'):
            mode=1
        else:
            mode=0
        self.writeCmd(f'bm{mode:1}')
        return

    def set_sweep_control(self,sweep_control):
        if(sweep_control == 'stop'):
            ctrl=0
        elif(sweep_control == 'start'):
            ctrl=1
        else:
            ctrl=0
        self.writeCmd(f'br{ctrl:1}')
        return

    def clear_internal_counter(self):
        self.writeCmd(f'bc')
        return

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

    def set_deputy_waveform(self,waveform):
        self.writeCmd(f'dw{waveform:1}')
        return

    def set_deputy_frequency(self,freqInHz):
        freq=int(freqInHz*100)
        self.writeCmd(f'df{freq:09d}')
        return

    def set_deputy_amplitude(self,ampl):
        self.writeCmd(f'da{ampl:2.1f}')
        return

    def set_deputy_DC_offset(self,offset):
        self.writeCmd(f'do{offset:3.1f}')
        return

    def set_deputy_wave_phase(self,phase):
        self.writeCmd(f'dp{phase:3}')
        return

    def set_deputy_duty_cycle(self,duty_cycle):
        duty=duty_cycle*10
        self.writeCmd(f'dd{duty:3}')
        return