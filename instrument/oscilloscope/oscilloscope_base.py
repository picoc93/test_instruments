#!/usr/bin/env python3
"""Oscilloscope Base Class"""

from abc import abstractmethod
from instrument import *


class Oscilloscope(Instrument):
    """Base class for oscilloscope instruments."""
    
    @abstractmethod
    def run(self):
        """Start acquisition."""
        pass
    
    @abstractmethod
    def stop(self):
        """Stop acquisition."""
        pass
    
    @abstractmethod
    def set_timebase_scale(self, scale: float):
        """Set horizontal timebase scale in seconds per division."""
        pass
    
    @abstractmethod
    def set_trigger_mode(self, mode):
        """Set trigger mode."""
        pass
    
    @abstractmethod
    def set_trigger_level(self, level: float):
        """Set trigger level in volts."""
        pass
    
    @abstractmethod
    def channel_scale(self, channel: int, scale: float):
        """Set vertical scale for a channel in volts per division."""
        pass
    
    @abstractmethod
    def measure_frequency(self) -> str:
        """Measure frequency."""
        pass
    
    @abstractmethod
    def measure_voltage_peak_to_peak(self) -> str:
        """Measure peak-to-peak voltage."""
        pass
