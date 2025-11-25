#!/usr/bin/env python3
import instrument

class Bench:

  def __init__(self,bench_id):
    self.id=bench_id
    self.power_supply = None
    self.function_generator=None
    self.oscilloscope=None

  def connect_power_supply(self,port):
    self.power_supply=instrument.psu.Owon(port)
    self.power_supply.connect(115200)

  def connect_function_generator(self,port):
    self.function_generator=instrument.awg.FeelTech(port)
    self.function_generator.connect(9600)

  def connect_oscilloscope(self,port):
    self.oscilloscope=instrument.oscilloscope.GWInstek(port)
    self.oscilloscope.connect(9600)

  def disconnect_psu(self):
    del self.power_supply

  def disconnect_function_generator(self):
    del self.function_generator

  def disconnect_oscilloscope(self):
    del self.oscilloscope
