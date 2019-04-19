# Author Brendan Horan
# License : BSD 3-Clause
# Description : Read the DF robot HK-A5 Laser PM2.5 sensor

import struct
from machine import UART


"""PM2.5 sensor, read the three pm values from the sensor

Exported class's:
PM25Base -- Used to Initialize the sensor
PM25_sensor -- Get the three PM values (1.0, 2.5, 10um)

"""


class PM25_serial_not_ready:
    pass


class PM25Base:
    def __init__(self, rx_pin, tx_pin):
        """Initialize the sensor.

        Keyword arguments:
        rx_pin -- pin number of the rx pin
        tx_pin -- pin number of the tx pin


        """

        # Set up the serial port according to the sensor docs
        uart = UART(1, 9600, timeout=0)
        uart.init(9600, bits=8, parity=None, stop=1, rx=rx_pin, tx=tx_pin)
        self.uart = uart


class PM25_sensor(PM25Base):
    def read_sensor(self):
        """Read the serial line data till we find the data.

        Returns:
        tuple -- pm1, pm2, pm10

        """

        test_serial = self.uart.read(1)
        if len(test_serial) == 0:
            byte, lastbyte = str.encode("\x00"), str.encode("\x00")
        else:
            raise PM25_serial_not_ready("can't read UART data")

        while True:
            lastbyte = byte
            byte = self.uart.read(1)
            # Start characters are 0x42 followed by 0x4d
            if lastbyte == str.encode("\x42") and byte == str.encode("\x4d"):
                # unpack 13 ints of data
                raw_data = self.uart.read(31)
                data = struct.unpack(">hhhhhhhhhhhhhhh", raw_data)

            # First, second and third bytes should be the sensor readings
            pm1 = data[1]
            pm2 = data[2]
            pm10 = data[3]
            return (pm1, pm2, pm10)
