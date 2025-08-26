#!/usr/bin/env python3

import serial
from enum import Enum

class Voltage_Scale(float, Enum):
  mV_1=0.002
  mV_2=0.005
  mV_10=0.01
  mV_20=0.02
  mV_50=0.05
  mV_100=0.1
  mV_200=0.2 
  mV_500=0.5
  V_1=1
  V_2=2
  V_5=5

#Sec/div	NR3
class Time_Scale(float, Enum):
  ns_1=1e-9
  ns_2_5=2.5e-9
  ns_5=5e-9
  ns_10=1e-8
  ns_25=2.5e-8
  ns_50=5e-8
  ns_100=1e-7
  ns_250=2.5e-7
  ns_500=5e-7
  us_1=1e-6
  us_2_5=2.5e-6
  us_5=5e-6
  us_10=1e-5
  us_25=2.5e-5
  us_50=5e-5
  us_100=1e-4
  us_250=2.5e-4
  us_500=5e-4
  ms_1=1e-3
  ms_2_5=2.5e-3
  ms_5=5e-3
  ms_10=1e-2
  ms_25=2.5e-2
  ms_50=5e-2
  ms_100=1e-1
  ms_250=2.5e-1
  ms_500=5e-1
  s_1=1
  s_2_5=2.5
  s_5=5
  s_10=10

class Acquire_Mode(IntEnum):
  sample_mode=0 
  peak_detection_mode=1
  average_mode=2

class Acquire_Average(IntEnum):
  ave_2=1
  ave_4=2
  ave_8=3
  ave_16=4
  ave_32=5
  ave_64=6
  ave_128=7
  ave_256=8

class Acquire_Length(IntEnum):
  len_500=0
  len_1250=1
  len_2500=2
  len_5000=3
  len_12500=4
  len_25000=5
  len_50000=6
  len_125000=7

class Channel(IntEnum):
  ch1=1
  ch2=2

class Channel_Coupling(IntEnum):
  AC=0 
  DC=1 
  Ground=2

class Channel_Probe(IntEnum):
  X_1=0 
  X_10=1 
  X_100=2

class Channel_Math(IntEnum):
  add_operator=0
  subtractor_operator=1
  FFT=2
  turn_off=3

class Trigger_Mode(IntEnum):
  auto_level=0
  auto=1
  normal=2
  single=3

class Trigger_Type(IntEnum):
  edge=0 
  video=1 
  pulse=2 
  delay=3

class Trigger_Source(IntEnum):
  ch1=0 
  ch2=1 
  external=2 
  AC_line_voltage=3

class Trigger_Coupling(IntEnum):
  AC=0 
  DC=1 

class Trigger_Slope(IntEnum):
  rising_slope=0
  falling_slope=1 

class Trigger_Video_Polarity(IntEnum):
  positive=0
  negative=1 


class GWInstek:

  def __init__(self, port, default_timeout=0.5):
    self.ser = None
    self.port = port
    self.timeout = default_timeout

  def open(self):
    self.ser = serial.Serial(self.port, 9600, timeout=self.timeout)
    self.identity = self.read_identity()

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

  def clear_event_registers(self):
    return self._cmd("*CLS")
  
  def get_event_status_enable_register(self):
    return self._cmd("*ESE?")
 
  def get_event_status_register(self):
    return self._cmd("*ESR?")
  
  def get_status_byte_register(self):
    return self._cmd("*STB?")

  def get_oscilloscope_settings(self):
    return self._cmd("*LRN?")
  
  def reset_oscilloscope_settings(self):
    return self._cmd("*RST")
  
  def is_operation_complete(self):
    return self._cmd("*OPC?")
  
  #Perform an automatic setup in order to optimize the acquisition parameters.
  def perform_autoset(self):
    return self._cmd("AUToset")

  #Controls the RUN state of trigger system. The acquisition cycle will follow each qualified trigger in the RUN state.
  def run(self):
    return self._cmd(":RUN")
  
  #Controls the STOP state of trigger system. The acquisition cycle only triggered when the :RUN command is received.
  def stop(self):
    return self._cmd(":STOP")

  #Select the waveform acquisition mode. There are four different acquisition mode: sample, peak detection, average and accumulate.
  #0→Select the sample mode 
  #1→Select the peak detection mode
  #2→Select the average mode
  def acquire_mode(self,number):
    return self._cmd(f":ACQuire:MODe {number}")

  #Select the average number of waveform acquisition. The range for averaging is from 2 to 256 in powers of 2.
  #1→Average number is 2 2→Average number is 4
  #3→Average number is 8 4→Average number is 16
  #5→Average number is 32 6→Average number is 64
  #7→Average number is 128 8→Average number is 256
  def acquire_average(self,number):
    return self._cmd(f":ACQuire:AVERage {number}")

  #Select the number of record length. This oscilloscope provides record length of 500, 1250, 2500, 5000, 12500, 25000, 50000, and 125000.
  #0→Record length is 500 1→Record length is 1250 2→Record length is 2500
  #3→Record length is 5000 4→Record length is 12500 5→Record length is 25000
  #6→Record length is 50000 7→Record length is 125000
  def acquire_length(self,number):
    return self._cmd(f":ACQuire:LENGth {number}")

  #<X>→Specify the channel number (1|2)
  def acquire_memory(self,channel):
    return self._cmd(f":ACQuire<{channel}>:MEMory?")

  #Transfer the displayed waveform data (always 500 points data totally) from the oscilloscope. Each point is composed by two bytes (the integer value of 16 bits). The high byte (MSD) will be prior transferred.
  #<X>→Specify the channel number (1|2)
  def acquire_point(self,channel):
    return self._cmd(f":ACQuire<{channel}>:POINt")

  #Sets the horizontal position (delay timebase) parameter.
    #Sec/div	NR3
  #1ns	1.00E-09
  #2.5ns	2.50E-09
  #5ns	5.00E-09
  #10ns	1.00E-08
  #25ns	2.50E-08
  #50ns	5.00E-08
  #100ns	1.00E-07
  #250ns	2.50E-07
  #500ns	5.00E-07
  #1μs	1.00E-06
  #2.5μs	2.50E-06
  #5μs	5.00E-06
  #10μs	1.00E-05
  #25μs	2.50E-05
  #50μs	5.00E-05
  #100μs	1.00E-04
  #250μs	2.50E-04
  #500μs	5.00E-04
  #1ms	1.00E-03
  #2.5ms	2.50E-03
  #5ms	5.00E-03
  #10ms	1.00E-02
  #25ms	2.50E-02
  #50ms	5.00E-02
  #100ms	1.00E-01
  #250ms	2.50E-01
  #500ms	5.00E-01
  #1s	1
  #2.5s	2.5
  #5s	5
  #10s	10
  def set_timebase_delay(self,delay):
    return self._cmd(f":TIMebase:DELay {delay}")
  
  #Sets the horizontal timebase scale per division (SEC/DIV).
  #Sec/div	NR3
  #1ns	1.00E-09
  #2.5ns	2.50E-09
  #5ns	5.00E-09
  #10ns	1.00E-08
  #25ns	2.50E-08
  #50ns	5.00E-08
  #100ns	1.00E-07
  #250ns	2.50E-07
  #500ns	5.00E-07
  #1μs	1.00E-06
  #2.5μs	2.50E-06
  #5μs	5.00E-06
  #10μs	1.00E-05
  #25μs	2.50E-05
  #50μs	5.00E-05
  #100μs	1.00E-04
  #250μs	2.50E-04
  #500μs	5.00E-04
  #1ms	1.00E-03
  #2.5ms	2.50E-03
  #5ms	5.00E-03
  #10ms	1.00E-02
  #25ms	2.50E-02
  #50ms	5.00E-02
  #100ms	1.00E-01
  #250ms	2.50E-01
  #500ms	5.00E-01
  #1s	1
  #2.5s	2.5
  #5s	5
  #10s	10
  def set_timebase_scale(self,scale):
    return self._cmd(f":TIMebase:SCALe {scale}")

  #Select and query the trigger mode.
  #0→Auto Level
  #1→Auto
  #2→Normal
  #3→Single
  def set_trigger_mode(self,mode):
    return self._cmd(f":TRIGger:MODe {mode}")
  
  #Select and query the trigger type.
  #0→Edge 
  #1→Video 
  #2→Pulse 
  #3→Delay
  def set_trigger_type(self,trigger_type):
    return self._cmd(f":TRIGger:TYPe {trigger_type}")

  #Select and query the trigger source.
  #0→Channel 1 
  #1→Channel 2 
  #2→External trigger 
  #3→AC line voltage
  def set_trigger_source(self,source):
    return self._cmd(f":TRIGger:SOURce {source}")
 
  #Select and query the type of trigger coupling.
  #0→AC 
  #1→DC
  def set_trigger_couple(self,couple):
    return self._cmd(f":TRIGger:COUPle {couple}")
  
  #Select and query the trigger level.
  def set_trigger_level(self,level):
    return self._cmd(f":TRIGger:LEVel {level}")

  #Switch and query the rising or falling trigger slope.
  #0→Rising slope 
  #1→Falling slope 
  def set_trigger_slope(self,slope):
    return self._cmd(f":TRIGger:SLOP {slope}")
  
  #Select and query the specified line for video signal.
  def set_trigger_video_line(self,line):
    return self._cmd(f":TRIGger:VIDeo:LINe {line}")

  #Select and query the input video polarity.
  #0→Positive-going sync pulses
  #1→Negative-going sync pulses
  def set_trigger_video_polarity(self,polarity):
    return self._cmd(f":TRIGger:VIDeo:POLarity {polarity}")

  #Enable or disable the waveform invert function. 
  #<X>→Specify the channel number (1|2) 
  #0→Disable invert function 
  #1→Enable invert function 
  def enable_channel_invert(self,channel,invert):
    return self._cmd(f":CHANnel{channel}::INVert {invert}")

  #Enable or disable the bandwidth limit function.
  #<X>→Specify the channel number (1|2)
  #0→Disable bandwidth limit 
  # 1→Enable bandwidth limit
  def enable_channel_bw_limit(self,channel, bw_limit):
    return self._cmd(f":CHANnel{channel}:BWLimi {bw_limit}")

  #Select the different coupling states for the oscilloscope.
  #<X>→Specify the channel number (1|2)
  #0→Place scope in AC coupling state 
  #1→Place scope in DC coupling state
  #2→Place scope in grounding state
  def channel_coupling(self,channel,coupling):
    return self._cmd(f":CHANnel{channel}:BWLimi {coupling}")

  #Set the math expression.
  #<X>→Specify the channel number (1|2)
  #0→Select the add operator 
  #1→Select the subtract operator
  #2→Select the FFT operation 
  #3→Turn off math function
  def channel_math(self,channel,math):
    return self._cmd(f":CHANnel{channel}:MATH {math}")

  #Sets or query the offset voltage.
  #<X>→Specify the channel number (1|2)
  #<NR3> is the desired offset value in volts. The range is dependent on the scale the probe attenuation factor. The offset ranges are following:
  #0.002->2mV
  #0.005->2mV
  #0.01->10mV
  #0.02->20mV
  #0.05->50mV
  #0.1->100mV
  #0.2->200mV 
  #0.5->500mV
  #1->1V
  #2->2V
  #5->5V
  def channel_offset(self,channel,offset):
    return self._cmd(f":CHANnel{channel}:OFFSet {offset}")

  #Select the different probe attenuation factor.
  #<X>→Specify the channel number (1|2)
  #0→1X 
  #1→10X 
  #2→100X
  def channel_probe(self,channel,probe):
    return self._cmd(f":CHANnel{channel}:PROBe {probe}")

  #Sets or query the vertical scale of the specified channel.
  #<X>→Specify the channel number (1|2)
  #<NR3> is the desired gain value in volts per division. The range is 2mV/div to 5V/div (with 1X probe).
  #0.002->2mV
  #0.005->2mV
  #0.01->10mV
  #0.02->20mV
  #0.05->50mV
  #0.1->100mV
  #0.2->200mV 
  #0.5->500mV
  #1->1V
  #2->2V
  #5->5V
  def channel_scale(self,channel,scale):
    return self._cmd(f":CHANnel{channel}:SCALe {scale}")

  #Select the measured channel (channel 1 or 2). The default setting of measured channel is channel one.
  #1→Enable the measurement functions for channel 1
  #2→Enable the measurement functions for channel 2
  def measure_source(self, channel):
    return self._cmd(f":MEASure:SOURce  {channel}")

  #Return the value of timing measurement that taken for falling edge of the first pulse in the waveform.
  def measure_fall(self):
    return self._cmd(f":MEASure:FALL?")

  #Return the value of timing measurement that taken for rising edge of the first pulse in the waveform.
  def measure_rise(self):
    return self._cmd(f":MEASure:RISe?")
  
  #Return the value of timing measurement of the first negative pulse in the waveform.
  def measure_negative_pulse(self):
    return self._cmd(f":MEASure:NWIDth?")
  
  #Return the value of timing measurement of the first positive pulse in the waveform.
  def measure_positive_pulse(self):
    return self._cmd(f":MEASure:PWIDth?")
  
  #Return the ratio of the positive pulse width to the signal period
  def measure_pulse_width(self):
    return self._cmd(f":MEASure:PDUTy?")
  
  #Return the value of Frequency measurement.
  def measure_frequency(self):
    return self._cmd(f":MEASure:FREQuency?")
  
  #Return the timing value of period measurement.
  def measure_period(self):
    return self._cmd(f":MEASure:PERiod?")
  
  #Return the voltages of high value minus the low value.
  def measure_voltage_amplitude(self):
    return self._cmd(f":MEASure:VAMPlitude?")
  
  #Return the average voltages.
  def measure_voltage_average(self):
    return self._cmd(f":MEASure:VAVerage?")
  
  #Return the value of global high voltage.
  def measure_voltage_high(self):
    return self._cmd(f":MEASure:VHI?")
  
  #Return the value of global low voltage.
  def measure_voltage_low(self):
    return self._cmd(f":MEASure:VLO?")
  
  #Return the value of maximum amplitude.
  def measure_voltage_max(self):
    return self._cmd(f":MEASure:VMAX?")
  
  #Return the value of minimum amplitude.
  def measure_voltage_min(self):
    return self._cmd(f":MEASure:VMIN?")
  
  #Return the value of Vmax minus Vmin.
  def measure_voltage_peak_to_peak(self):
    return self._cmd(f":MEASure:VPP?")
  
  #Return the value of true Root Mean Square voltage.
  def measure_voltage_rms(self):
    return self._cmd(f":MEASure:VRMS?")
  