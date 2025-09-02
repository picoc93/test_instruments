#!/usr/bin/env python3

import serial
import io
import logging

###############################################################################
class Owon:
  
  def __init__(self, port,cmd_timeout=0.5):
    self.id=None
    self.serial_connection = None
    self.port=port
    self.timeout=cmd_timeout
    #self._serialIO = io.TextIOWrapper(io.BufferedRWPair(self._serial, self._serial), newline='')

  def __del__(self):
    if self.is_open():
        self.close()

  def open(self):
    self.serial_connection= serial.Serial(self.port, 115200, timeout=1)

  def is_open(self):
    return hasattr(self, 'serial_connection') and self.ser is not None

  def close(self):
    self.serial_connection.close()
  
  def __enter__(self):
    self.open()
    return self

  def __exit__(self, *args, **kwargs):
    self.close()
  
  def writeCmd(self, command):
    if not self.is_open():
        raise Exception("Connection is not open!")
      
    self.serial_connection.write(bytes(command, 'utf-8') + b"\n")
    ret = self.serial_connection.readline().decode('utf-8')
      
    if not ret.endswith("\r\n"):
        raise Exception(f"Wrong command ending: '{command}'!")
      
    return ret[:-2]
  
  def writeSilentCmd(self, command):

    if not self.is_open():
      raise Exception("Connection is not open!")
      
    self.serial_connection.write(bytes(command, 'utf-8') + b"\n")
    ret = self.serial_connection.readline().decode('utf-8')
      
    if ret[:-2] == "ERR":
      raise Exception(f"Error while executing command: '{command}'")

  def reset_serial_buffer(self):
    if not self.is_open():
        raise Exception("Connection is not open!")
    self.serial_connection.reset_input_buffer()
    self.serial_connection.reset_output_buffer()
  
  ###########################################################################
  def get_device_id(self):
    return self.writeCmd("*IDN?")

  def measure_voltage(self):
    return float(self.writeCmd("MEASure:VOLTage?"))

  def measure_current(self):
    return float(self.writeCmd("MEASure:CURRent?"))

  def get_voltage(self):
    return float(self.writeCmd("VOLTage?"))

  def get_current(self):
    return float(self.writeCmd("CURRent?"))

  def get_voltage_limit(self):
    return float(self.writeCmd("VOLTage:LIMit?"))

  def get_current_limit(self):
    return float(self.writeCmd("CURRent:LIMit?"))
  
  def set_voltage(self, voltage):
    return self.writeSilentCmd(f"VOLTage {voltage:.3f}")

  def set_current(self, current):
    return self.writeSilentCmd(f"CURRent {current:.3f}")

  def set_voltage_limit(self, voltage):
    return self.writeSilentCmd(f"VOLTage:LIMit {voltage:.3f}")

  def set_current_limit(self, current):
    return self.writeSilentCmd(f"CURRent:LIMit {current:.3f}")

  def get_output(self):
    ret = self.writeCmd(f"OUTPut?")

    if ret in ["0", "1"]:
      return ret == "1"
    if ret not in ["ON", "OFF"]:
      raise Exception(f"Unknown return for get output command: {ret}")
    return ret == "ON"

  def set_output(self, enabled):
    self.writeSilentCmd(f"OUTPut {'ON' if enabled else 'OFF'}")
    #System Control Commands: equivalent to 'Keylock' button on P4000 series

  #def set_keylock(self, enabled):
  #  if enabled:
  #  # Note: SYSTem:REMote does not work on P4603
  #  self.writeSilentCmd("SYST:REM")
  #  else:
  #  # Note: SYSTem:LOCal does not work on P4603
  #  self.writeSilentCmd("SYST:LOC")