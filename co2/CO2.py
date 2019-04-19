# Author Brendan Horan
# License : BSD 3-Clause
# Description : Read the DF robot co2 laser sensor

from machine import ADC, Pin

"""CO2_sensor, read then caculate the co2 concentration

Exported class's:
CO2_base -- Used to Initialize the sensor
CO2_sensor -- Get Co2 concentration (ppm)

"""


class CO2_sensor_not_ready():
    pass


class CO2_base:
    def __init__(self, pin):
        """Initialize the sensor.

        Keyword arguments:
        pin -- pin number of an ADC pin

        """

        self.pin = pin


class CO2_sensor(CO2_base):
    def read_sensor(self):
        """Get the Co2 reading, returns a float"""

        adc = ADC(Pin(self.pin))

        # set the ADC up
        # 12 bit wide, 11DB attenuation
        adc.atten(adc.ATTN_11DB)
        adc.width(adc.WIDTH_12BIT)

        sensorValue = adc.read()

        # Divide the voltage 3v3 by the ADC levels at 12bit
        voltage = sensorValue*(3300/4095.0)

        # Below taken from df robot site SKU : SEN0219 wiki
        voltage_diference = voltage-400
        concentration = voltage_diference*50.0/16.0
        if concentration > 0:
            return(concentration)
        else:
            raise CO2_sensor_not_ready("Co2 sensor not ready")
