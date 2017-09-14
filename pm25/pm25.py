# Author Brendan Horan
# License : BSD 3-Clause
# Description : Read the DF robot HK-A5 Laser PM2.5 sensor

import sys
import time
import struct
from machine import UART

class PM25Base:
  def __init__(self, rx_pin, tx_pin):
    uart = UART(1, 9600, timeout=0)
    uart.init(9600, bits=8, parity=None, stop=1, rx=rx_pin, tx=tx_pin)
    self.uart = uart

class PM25_sensor(PM25Base):
  def read_sensor(self):
    test_serial = self.uart.read(1)
    if len(test_serial) == 0:
      sys.exit()
    
    byte, lastbyte = str.encode("\x00"), str.encode("\x00")

    while True:
      lastbyte = byte
      byte = self.uart.read(1)
      if lastbyte == str.encode("\x42") and byte == str.encode("\x4d"):
        raw_data = self.uart.read(31)
        data = struct.unpack(">hhhhhhhhhhhhhhh",raw_data)

        pm1 = data[1]
        pm2 = data[2]
        pm10 = data[3]
        return (pm1, pm2, pm10)

