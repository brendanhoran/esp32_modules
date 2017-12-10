# Author Brendan Horan
# License : BSD 3-Clause
# Description : Set up a Wifi connection

import network
import sys
import time

class WIFI_Base:
  def __init__(self,ssid,password):
    self.ssid = ssid
    self.password = password

class WIFI_setup(WIFI_Base):
  def connect(self):

    print("Wifi setup beginning")
    wlan = network.WLAN(network.STA_IF); wlan.active(True)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(self.ssid, self.password)
    time.sleep(5)

    if wlan.isconnected() == False:
      print("WiFi not connected")
      wlan.disconnect()
    else:
      print("Wifi connected")
      print(wlan.ifconfig())
