# Author Brendan Horan
# License : BSD 3-Clause
# Description : Read the DF robot c02 laser sensor

import machine
from machine import ADC, Pin

class C02_base:
  def __init__(self, pin):
    self.pin = pin

class C02_sensor(Co2_base):
  def read_sensor(self):
    adc = ADC(Pin(self.pin))
    adc.atten(adc.ATTN_11DB)
    adc.width(adc.WIDTH_12BIT)
    sensorValue = adc.read()
    voltage = sensorValue*(3300/4095.0)
    voltage_diference=voltage-400
    concentration=voltage_diference*50.0/16.0
    return(concentration)
