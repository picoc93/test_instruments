#!/usr/bin/env python3
import instrument

###############################################################################
class Owon (instrument.Instrument):
  
  def __init__(self, port,cmd_timeout=0.5):
    super().__init__(port,cmd_timeout)

  def writeCmd(self, command):
    return super().writeCmd(command,"\r\n","\r\n")

  def writeSilentCmd(self, command):
    super().writeSilentCmd(command,"\r\n")
  
  def connect(self,baud_rate):
    super().connect(baud_rate)
    id=self.get_device_id()
    super().set_id(id)

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