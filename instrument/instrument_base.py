#!/usr/bin/env python3
"""
Instrument Base Class
Simple base class for all instruments with multi-connection support.
"""

from abc import ABC, abstractmethod
from connections import create_connection


class Instrument(ABC):
    """
    Base class for all instruments.
    
    Supports: Serial (ASRL), GPIB, TCPIP, USB
    
    Usage:
        instrument = MyInstrument("COM3")
        instrument.connect(baud_rate=9600)
        result = instrument.query("*IDN?")
        instrument.disconnect()
    """
    
    def __init__(self, resource_id: str, timeout: float = 1.0):
        """
        Initialize instrument.
        
        Args:
            resource_id: Connection string
                Examples:
                - "COM3" or "/dev/ttyUSB0" (Serial)
                - "ASRL1::INSTR" (Serial VISA format)
                - "GPIB0::1::INSTR" (GPIB)
                - "TCPIP::192.168.1.1::INSTR" (TCPIP)
                - "USB::0x1234::0x5678::INSTR" (USB)
            timeout: Timeout in seconds
        """
        self.resource_id = resource_id
        self.connection = create_connection(resource_id, timeout)
        self.device_id = None

    def connect(self, **kwargs):
        """Connect to instrument with error reporting."""
        try:
            self.connection.connect(**kwargs)
            self.device_id = self.get_device_id()
        except Exception as e:
            print(f"Connection failed for {self.resource_id}: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from instrument."""
        self.connection.disconnect()
    
    def is_connected(self) -> bool:
        """Check if connected."""
        return self.connection.is_connected()
    
    def write(self, command: str):
        """Write command to instrument."""
        self.connection.write(command)
    
    def read(self) -> str:
        """Read from instrument."""
        return self.connection.read()
    
    def query(self, command: str) -> str:
        """Write command and read response."""
        return self.connection.query(command)
    
    @abstractmethod
    def get_device_id(self) -> str:
        """Get device ID (must be implemented in subclass)."""
        pass

    def __enter__(self):
        """Context manager entry - now handles connection automatically."""
        if not self.is_connected():
            self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
        return False
    
    def __repr__(self) -> str:
        """String representation."""
        status = "connected" if self.is_connected() else "disconnected"
        return f"{self.__class__.__name__}('{self.resource_id}', {status})"
