#!/usr/bin/env python3

import serial
import io
import logging
logging.basicConfig(filename='./log/example.log',
                    filemode='w',# 'w' for write (overwrite), 'a' for append
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s', 
                    datefmt='%m/%d/%Y %I:%M:%S %p')

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

  def is_connected(self):
    return hasattr(self, 'serial_connection') and self.serial_connection is not None

  def close_connection(self):
    self.serial_connection.close()

  def set_id(self,id):
    self.id=id

  def writeCmd(self, command, tx_end_string, rx_end_string):
    if not self.is_connected():
      raise Exception("Connection is not open!")

    if(self.id is not None):
      self.serial_connection.write(bytes(command+tx_end_string, 'utf-8'))
      logging.info("->"+self.id+": "+command)   
      ret = self.serial_connection.readline().decode('utf-8')
      logging.info("<-"+self.id+": "+ret)
    else:
      self.serial_connection.write(bytes(command+tx_end_string, 'utf-8'))
      logging.info("-> "+command)   
      ret = self.serial_connection.readline().decode('utf-8')
      logging.info("<- "+ret)
        
    if not ret.endswith(rx_end_string):
     raise Exception(f"Wrong command ending: '{command}'!")
    
    n=len(rx_end_string)
    return ret[:-n]

  def writeSilentCmd(self, command,tx_end_string):
    if not self.is_connected():
      raise Exception("Connection is not open!")
    
    logging.info("->"+self.id+": "+command)
    self.serial_connection.write(bytes(command+tx_end_string, 'utf-8') )
    ret = self.serial_connection.readline().decode('utf-8')
        
    if ret[:-2] == "ERR":
      raise Exception(f"Error while executing command: '{command}'")
    
  def reset_serial_buffer(self):
    if not self.is_connected():
      raise Exception("Connection is not open!")
    self.serial_connection.reset_input_buffer()
    self.serial_connection.reset_output_buffer()
    

