#!/usr/bin/env python3
"""PSU Base Class"""

from abc import abstractmethod
from instrument import Instrument


class PSU(Instrument):
    """Base class for PSU instruments."""
    
    @abstractmethod
    def set_voltage(self, voltage: float):
        pass
    
    @abstractmethod
    def set_current(self, current: float):
        pass
    
    @abstractmethod
    def get_voltage(self) -> float:
        pass
    
    @abstractmethod
    def get_current(self) -> float:
        pass
    
    @abstractmethod
    def measure_voltage(self) -> float:
        pass
    
    @abstractmethod
    def measure_current(self) -> float:
        pass
    
    @abstractmethod
    def set_output(self, enabled: bool):
        pass
    
    @abstractmethod
    def get_output(self) -> str:
        pass
