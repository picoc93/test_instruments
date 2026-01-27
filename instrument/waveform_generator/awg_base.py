#!/usr/bin/env python3
"""AWG Base Class"""

from abc import abstractmethod
from instrument import Instrument


class AWG(Instrument):
    """Base class for Arbitrary Waveform Generator instruments."""
    
    @abstractmethod
    def set_waveform(self, waveform):
        """Set output waveform type."""
        pass
    
    @abstractmethod
    def set_frequency(self, freq_hz: float):
        """Set output frequency in Hz."""
        pass
    
    @abstractmethod
    def set_amplitude(self, amplitude: float):
        """Set output amplitude in volts."""
        pass
    
    @abstractmethod
    def set_DC_offset(self, offset: float):
        """Set DC offset in volts."""
        pass
    
    @abstractmethod
    def get_frequency(self) -> str:
        """Get current frequency."""
        pass
