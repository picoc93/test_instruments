#!/usr/bin/env python3
"""
Connection Manager
Handles Serial, GPIB, TCPIP, and USB connections using an Abstract Base Class.
"""
import pyvisa
import serial
from abc import ABC, abstractmethod
from typing import Any


class BaseConnection(ABC):
    """Abstract Base Class for all instrument connections."""

    def __init__(self, resource_id: str, timeout: float = 1.0):
        self.resource_id = resource_id
        self.timeout = timeout
        self.connection: Any = None

    @abstractmethod
    def connect(self, **kwargs):
        """Establish the connection."""
        pass

    @abstractmethod
    def disconnect(self):
        """Close the connection."""
        pass

    @abstractmethod
    def write(self, data: str):
        """Send data to the instrument."""
        pass

    @abstractmethod
    def read(self) -> str:
        """Read data from the instrument."""
        pass

    def query(self, command: str) -> str:
        """Standard Write-Read operation."""
        self.write(command)
        return self.read()

    def is_connected(self) -> bool:
        """Check if connection exists."""
        return self.connection is not None


class SerialConnection(BaseConnection):
    """Serial connection handler using pyserial."""

    def __init__(self, resource_id: str, timeout: float = 1.0):
        super().__init__(resource_id, timeout)
        # Logic to convert ASRL strings to COM/tty if needed
        if "ASRL" in self.resource_id.upper():
            port_num = self.resource_id.split("::")[0].upper().replace("ASRL", "")
            self.port = f"COM{port_num}" if port_num.isdigit() else port_num
        else:
            self.port = resource_id

    def connect(self, baud_rate: int = 9600, **kwargs):
        self.connection = serial.Serial(
            self.port, baud_rate, timeout=self.timeout, **kwargs
        )

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def write(self, data: str):
        self.connection.write(data.encode())
        self.connection.flush()

    def read(self) -> str:
        return self.connection.readline().decode().strip()

    def is_connected(self) -> bool:
        return self.connection and self.connection.is_open


class VISAConnection(BaseConnection):
    """Unified handler for GPIB, USB, and TCPIP via PyVISA."""

    def connect(self, **kwargs):
        rm = pyvisa.ResourceManager()
        self.connection = rm.open_resource(self.resource_id)
        self.connection.timeout = int(self.timeout * 1000)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def write(self, data: str):
        self.connection.write(data)

    def read(self) -> str:
        return self.connection.read().strip()

    def query(self, command: str) -> str:
        # Override with native VISA query for better performance
        return self.connection.query(command).strip()


def create_connection(resource_id: str, timeout: float = 1.0) -> BaseConnection:
    """Factory to create the appropriate connection type."""
    res = resource_id.upper()

    if any(x in res for x in ["COM", "/DEV/TTY", "ASRL"]):
        return SerialConnection(resource_id, timeout)
    elif any(x in res for x in ["GPIB", "TCPIP", "USB"]):
        return VISAConnection(resource_id, timeout)
    else:
        raise ValueError(f"Unknown connection type: {resource_id}")