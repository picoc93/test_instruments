#!/usr/bin/env python3
"""GW Instek GDS-806S Driver - Simplified"""

from enum import IntEnum
from oscilloscope_base import Oscilloscope


class Channel(IntEnum):
    """Oscilloscope channels."""
    CH1 = 1
    CH2 = 2


class TriggerMode(IntEnum):
    """Trigger modes."""
    AUTO_LEVEL = 0
    AUTO = 1
    NORMAL = 2
    SINGLE = 3

class GWInstekGDS806S(Oscilloscope):
    """GW Instek GDS-806S 60MHz oscilloscope driver."""
    
    def get_device_id(self) -> str:
        """Get device ID."""
        return self.query("*IDN?\n")
    
    def run(self):
        """Start acquisition."""
        self.write(":RUN\n")
    
    def stop(self):
        """Stop acquisition."""
        self.write(":STOP\n")
    
    def set_timebase_scale(self, scale: float):
        """Set timebase scale (seconds per division)."""
        self.write(f":TIMebase:SCALe {scale}\n")
    
    def set_trigger_mode(self, mode: TriggerMode):
        """Set trigger mode."""
        self.write(f":TRIGger:MODe {int(mode)}\n")
    
    def set_trigger_level(self, level: float):
        """Set trigger level (volts)."""
        self.write(f":TRIGger:LEVel {level}\n")
    
    def channel_scale(self, channel: Channel, scale: float):
        """Set channel vertical scale (volts per division)."""
        self.write(f":CHANnel{int(channel)}:SCALe {scale}\n")
    
    def measure_frequency(self) -> str:
        """Measure frequency."""
        return self.query(":MEASure:FREQuency?\n")
    
    def measure_voltage_peak_to_peak(self) -> str:
        """Measure peak-to-peak voltage."""
        return self.query(":MEASure:VPP?\n")
    
    def measure_source(self, channel: Channel):
        """Select measurement source channel."""
        self.write(f":MEASure:SOURce {int(channel)}\n")
    
    def perform_autoset(self):
        """Perform automatic setup."""
        self.write("AUToset\n")
