#!/usr/bin/env python3

import instrument.awg.fy3224s as fg;
import instrument.psu.owon_spm3051 as psu;
import instrument.oscilloscope.gw_instek_gds_806s as osc;

###############################################################################
class Bench:
  
  def __init__(self,bench_id):
    self.id=bench_id
    self.power_supply = None
    self.function_generator=None
    self.oscilloscope=None

  def connect_psu(self,port):
    self.power_supply=psu.Owon(port)

  def connect_function_generator(self,port):
    self.function_generator=fg.FeelTech(port)

  def connect_oscilloscope(self,port):
    self.oscilloscope=osc.GWInstek(port)