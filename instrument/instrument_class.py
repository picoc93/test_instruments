#!/usr/bin/env python3

import serial
import io
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

###############################################################################
class Instrument:

  def __init__(self, port, default_timeout=0.5):
    self.id=None
    self.serial_connection = None
    self.port = port
    self.timeout = default_timeout

  def __del__(self):
    if self.is_connected():
      self.close_connection()  

  def connect(self,baud_rate):
    self.serial_connection = serial.Serial(self.port, baud_rate, timeout=self.timeout)
    self.id = self.get_device_id()

  def is_connected(self):
     return hasattr(self, 'serial_connection') and self.serial_connection is not None

  def close_connection(self):
    self.serial_connection.close()

  def __enter__(self):
    self.connect()
    return self

  def __exit__(self, *args, **kwargs):
    self.close_connection()

  def writeCmd(self, command, end_string):
    if not self.is_connected():
      raise Exception("Connection is not open!")
   
    logging.INFO("->"+self.id+": "+command)    
    self.serial_connection.write(bytes(command+end_string, 'utf-8'))
    ret = self.serial_connection.readline().decode('utf-8')
    logging.INFO("<-"+self.id+": "+ret)
        
    if not ret.endswith(end_string):
      raise Exception(f"Wrong command ending: '{command}'!")
        
    return ret[:-2]

  def writeSilentCmd(self, command,end_string):
    if not self.is_connected():
      raise Exception("Connection is not open!")
    
    logging.INFO("->"+self.id+": "+command)
    self.serial_connection.write(bytes(command+end_string, 'utf-8') )
    ret = self.serial_connection.readline().decode('utf-8')
        
    if ret[:-2] == "ERR":
      raise Exception(f"Error while executing command: '{command}'")
    
  def reset_serial_buffer(self):
    if not self.is_connected():
      raise Exception("Connection is not open!")
    self.serial_connection.reset_input_buffer()
    self.serial_connection.reset_output_buffer()
    

