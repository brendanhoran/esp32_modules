# Author Brendan Horan
# License : BSD 3-Clause
# Description : Set up a Wifi connection

import network
from time import sleep

"""WiFi setup wrapper, used to set up a connection

Exported class's:
WIFI_Base -- Used to set SSID name and password
WIFI_setup -- Tries to establish a connection

"""


class WiFi_connection_issue(Exception):
    pass


class WIFI_Base:
    def __init__(self, ssid, password):
        """Set SSID name and password

        Keyword arguments:
        ssid -- The SSID name
        password -- The password for the network

        """

        self.ssid = ssid
        self.password = password


class WIFI_setup(WIFI_Base):
    def connect(self):
        """Attempt to connect to WiFi network"""

        print("Wifi setup beginning")
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(self.ssid, self.password)

        # takes around 5 seconds for the esp32 to negotiate
        sleep(5)

        # .status() on esp32 returns "none".. Always...
        # only choice we have is to see if its connected
        # this also means we can't know why the connection failed
        if wlan.isconnected() is True:
            print("connected:")
            print(wlan.ifconfig())
        else:
            wlan.disconnect()
            raise WiFi_connection_issue("Could not connect to AP")
