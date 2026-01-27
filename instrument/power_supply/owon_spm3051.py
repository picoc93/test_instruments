#!/usr/bin/env python3
"""Owon SPM3051 Driver - Simplified"""

from psu_base import PSU


class OwonSPM3051(PSU):
    """Simple Owon SPM3051 driver."""
    
    def get_device_id(self) -> str:
        return self.query("*IDN?\r\n")
    
    def set_voltage(self, voltage: float):
        self.write(f"VOLTage {voltage:.3f}\r\n")
    
    def set_current(self, current: float):
        self.write(f"CURRent {current:.3f}\r\n")
    
    def get_voltage(self) -> float:
        return float(self.query("VOLTage?\r\n"))
    
    def get_current(self) -> float:
        return float(self.query("CURRent?\r\n"))
    
    def measure_voltage(self) -> float:
        return float(self.query("MEASure:VOLTage?\r\n"))
    
    def measure_current(self) -> float:
        return float(self.query("MEASure:CURRent?\r\n"))
    
    def set_output(self, enabled: bool):
        self.write(f"OUTPut {'ON' if enabled else 'OFF'}\r\n")
    
    def get_output(self) -> str:
        return self.query("OUTPut?\r\n")
