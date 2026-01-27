#!/usr/bin/env python3
"""FeelTech FY3224S Driver - Simplified"""

from enum import IntEnum
from awg_base import AWG


class Waveform(IntEnum):
    """Waveform types."""
    SINE = 0
    SQUARE = 1
    PULSE = 2
    TRIANGULAR = 3
    SAWTOOTH = 4
    FALL_SAWTOOTH = 5
    DC = 6

class FeelTechFY3224S(AWG):
    """FeelTech FY3224S 2-channel 25MHz AWG driver."""
    
    def get_device_id(self) -> str:
        """Get device ID."""
        return self.query('a\r\n')
    
    def set_waveform(self, waveform: Waveform):
        """Set waveform type."""
        self.write(f'bw{int(waveform):01d}\r\n')
    
    def set_frequency(self, freq_hz: float):
        """Set frequency in Hz."""
        freq = int(freq_hz * 100)
        self.write(f'bf{freq:09d}\r\n')
    
    def set_amplitude(self, amplitude: float):
        """Set amplitude in volts."""
        self.write(f'ba{amplitude:04.1f}\r\n')
    
    def set_DC_offset(self, offset: float):
        """Set DC offset in volts."""
        self.write(f'bo{offset:+04.1f}\r\n')
    
    def get_frequency(self) -> str:
        """Get current frequency."""
        return self.query('cf\r\n')
    
    def set_duty_cycle(self, duty_cycle: float):
        """Set duty cycle (0-100%)."""
        duty = int(duty_cycle * 10)
        self.write(f'bd{duty:04d}\r\n')
    
    def set_deputy_waveform(self, waveform: Waveform):
        """Set channel 2 waveform."""
        self.write(f'dw{int(waveform):01d}\r\n')
    
    def set_deputy_frequency(self, freq_hz: float):
        """Set channel 2 frequency."""
        freq = int(freq_hz * 100)
        self.write(f'df{freq:09d}\r\n')
    
    def set_deputy_amplitude(self, amplitude: float):
        """Set channel 2 amplitude."""
        self.write(f'da{amplitude:04.1f}\r\n')
