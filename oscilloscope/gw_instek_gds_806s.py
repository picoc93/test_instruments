#!/usr/bin/env python3

import serial
import io
from enum import IntEnum
import time;

import serial

class GWInstek:

  def __init__(self, port, default_timeout=0.5):
    self.ser = None
    self.port = port
    self.timeout = default_timeout

  def open(self):
    self.ser = serial.Serial(self.port, 9600, timeout=self.timeout)
    identity = self.read_identity()

  def close(self):
    self.ser.close()

  def __enter__(self):
    self.open()
    return self

  def __exit__(self, *args, **kwargs):
    self.close()

  def _cmd(self, command, accept_silent=False, timeout=None):
    if self.ser == None:
      raise Exception("Connection is not open!")
    self.ser.write(bytes(command, 'utf-8') + b"\n")
    self.ser.timeout = timeout if timeout is not None else self.timeout
    ret = self.ser.readline().decode('utf-8')
    #ret.endswith("\r\n")
    if not ret.endswith("\n") and not accept_silent:
      raise Exception(f"No response for command: '{command}'!")
    return ret[:-2]

  def _silent_cmd(self, command, timeout=0.01):
    if self._cmd(command, accept_silent=True, timeout=timeout) == "ERR":
      raise Exception(f"Error while executing command: '{command}'")

  def read_identity(self):
    return self._cmd("*IDN?")
