#!/usr/bin/env python3

import serial

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
    return self._cmd(f":ACQuire:MODe{number}")

  #Select the average number of waveform acquisition. The range for averaging is from 2 to 256 in powers of 2.
  #1→Average number is 2 2→Average number is 4
  #3→Average number is 8 4→Average number is 16
  #5→Average number is 32 6→Average number is 64
  #7→Average number is 128 8→Average number is 256
  def acquire_average(self,number):
    return self._cmd(f":ACQuire:AVERage{number}")

  #Select the number of record length. This oscilloscope provides record length of 500, 1250, 2500, 5000, 12500, 25000, 50000, and 125000.
  #0→Record length is 500 1→Record length is 1250 2→Record length is 2500
  #3→Record length is 5000 4→Record length is 12500 5→Record length is 25000
  #6→Record length is 50000 7→Record length is 125000
  def acquire_length(self,number):
    return self._cmd(f":ACQuire:LENGth{number}")

  #(The memory capacity can be selected as 500, 1250, 2500, 5000, 12500, 25000, 50000, or 125000 points
  #<X>→Specify the channel number (1|2)
  def acquire_memory(self,channel):
    return self._cmd(f":ACQuire<{channel}>:MEMory?")

  #Transfer the displayed waveform data (always 500 points data totally) from the oscilloscope. Each point is composed by two bytes (the integer value of 16 bits). The high byte (MSD) will be prior transferred.
  #<X>→Specify the channel number (1|2)
  def acquire_point(self,channel):
    return self._cmd(f":ACQuire<{channel}>:POINt")

  #Sets the horizontal position (delay timebase) parameter.
  def set_timebase_delay(self,delay):
    return self._cmd(f":TIMebase:DELay {delay}")
  
  #Sets the horizontal timebase scale per division (SEC/DIV).
  def set_timebase_scale(self,scale):
    return self._cmd(f":TIMebase:SCALe {scale}")

  #Select and query the trigger mode.
  #0→Auto Level
  #1→Auto
  #2→Normal
  #3→Single
  def set_trigger_mode(self,mode):
    return self._cmd(f":TRIGger:MODe  {mode}")
  
  #Select and query the trigger type.
  def set_trigger_type(self,type):
    return self._cmd(f":TRIGger:TYPe  {type}")

  #Select and query the trigger source.
  def set_trigger_source(self,source):
    return self._cmd(f":TRIGger:SOURce  {source}")
 
  #Select and query the type of trigger coupling.
  #0→AC 1→DC
  def set_trigger_couple(self,couple):
    return self._cmd(f":TRIGger:COUPle  {couple}")
  
  #Select and query the trigger level.
  def set_trigger_level(self,level):
    return self._cmd(f":TRIGger:LEVel  {level}")

  #Switch and query the rising or falling trigger slope.
  def set_trigger_slope(self,slope):
    return self._cmd(f":TRIGger:SLOP  {slope}")
  
  #Select and query the specified line for video signal.
  def set_trigger_video_line(self,line):
    return self._cmd(f":TRIGger:VIDeo:LINe  {line}")

  #Select and query the input video polarity.
  #0→Positive-going sync pulses
  #1→Negative-going sync pulses
  def set_trigger_video_polarity(self,polarity):
    return self._cmd(f":TRIGger:VIDeo:POLarity  {polarity}")

  #Enable or disable the bandwidth limit function.
  #0→Disable bandwidth limit 1→Enable bandwidth limit
  #<X>→Specify the channel number (1|2)
  def enable_bw_limit(self,channel, bw_limit):
    return self._cmd(f":CHANnel{channel}:BWLimi  {bw_limit}")

  #Select the different coupling states for the oscilloscope.
  #<X>→Specify the channel number (1|2)
  #0→Place scope in AC coupling state 1→Place scope in DC coupling state
  #2→Place scope in grounding state
  def channel_coupling(self,channel,coupling):
    return self._cmd(f":CHANnel{channel}:BWLimi  {coupling}")

  #Set the math expression.
  #<X>→Specify the channel number (1|2)
  #0→Select the add operator 1→Select the subtract operator
  #2→Select the FFT operation 3→Turn off math function
  def channel_math(self,channel,math):
    return self._cmd(f":CHANnel{channel}:MATH {math}")

  #Sets or query the offset voltage.
  #<X>→Specify the channel number (1|2)
  #<NR3> is the desired offset value in volts. The range is dependent on the scale the probe attenuation factor. The offset ranges are following:
  def channel_offset(self,channel,offset):
    return self._cmd(f":CHANnel{channel}:OFFSet {offset}")

  #Select the different probe attenuation factor.
  #<X>→Specify the channel number (1|2)
  #0→1X 1→10X 2→100X
  def channel_probe(self,channel,probe):
    return self._cmd(f":CHANnel{channel}:PROBe {probe}")

  #Sets or query the vertical scale of the specified channel.
  #<X>→Specify the channel number (1|2)
  #<NR3> is the desired gain value in volts per division. The range is 2mV/div to 5V/div (with 1X probe).
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
  