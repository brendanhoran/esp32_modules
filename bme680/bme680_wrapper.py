# Author Brendan Horan
# License : BSD 3-Clause
# Description : Read the DF robot bme680 sensor

import bme680
from i2c import I2CAdapter
import machine
from time import sleep

"""BME60_wrapper , read values from the BME680 sensor easily

Exported class's:
BME680Base -- Use to Initialize the sensor
read_temperature -- Get temperature (Celsius)
read_pressure -- Get pressure reading (hPa)
read_gas_resistance -- Get gas reading (ohms)
read_humidity -- Read the humidity (relative humidity)
read_iaq -- Calculate the current IAQ (0-100%)

"""


class SensorUnstable(Exception):
    pass


class SensorPolling(Exception):
    pass


class BME680Base:
    def __init__(self, scl_pin, sda_pin):
        """Initialize the sensor.

        Keyword arguments:
        scl_pin -- pin number of the I2C Serial Clock line
        sda_pin -- pin number of the I2C Serial Data line

        """

        i2c_dev = I2CAdapter(scl=machine.Pin(scl_pin),
                             sda=machine.Pin(sda_pin))
        sensor = bme680.BME680(i2c_device=i2c_dev)
        self.sensor = sensor

        # Set up the over sampling and filters
        # refer to the BME680 docs
        # The values below are good balance
        # between sensitivity and refresh
        sensor.set_humidity_oversample(bme680.OS_2X)
        sensor.set_pressure_oversample(bme680.OS_4X)
        sensor.set_temperature_oversample(bme680.OS_8X)
        sensor.set_filter(bme680.FILTER_SIZE_3)

        # Configure the gas sensor
        # refer to the BME680 docs
        # values mostly taken from that as defaults
        sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        sensor.set_gas_heater_temperature(320)
        sensor.set_gas_heater_duration(150)
        sensor.select_gas_heater_profile(0)


class BME680_sensor(BME680Base):
    def _get_sensor_data(self):
        """Get the sensor data, returns a tuple

        Returns:
        tuple -- temperature, pressure, gas_resistance, humidity

        """

        sensor_data = self.sensor.get_sensor_data()
        heater_stable = self.sensor.data.heat_stable
        if sensor_data and heater_stable:
            temperature = self.sensor.data.temperature
            pressure = self.sensor.data.pressure
            gas_resistance = self.sensor.data.gas_resistance
            humidity = self.sensor.data.humidity
            return (temperature, pressure, gas_resistance, humidity)
        else:
            raise SensorUnstable("Sensor not ready")

    def read_temperature(self):
        """Get the temperature reading, returns a float"""

        temperature = self._get_sensor_data()[0]
        return (temperature)

    def read_pressure(self):
        """Get the pressure reading, returns a float"""

        pressure = self._get_sensor_data()[1]
        return (pressure)

    def read_gas_resistance(self):
        """Get the gas reading in ohms, returns a float"""

        gas_resistance = self._get_sensor_data()[2]
        return(gas_resistance)

    def read_humidity(self):
        """Get the humidity reading, returns a float"""

        humidity = self._get_sensor_data()[3]
        return (humidity)

    def _get_iaq_data(self):
        """Get gas and humidity readings for IAQ, returns a tuple

        Returns:
        tuple -- gas_resistance, humidity

        """

        reading = None
        try:
            reading = self._get_sensor_data()[2:4]
            return(reading)
        except IndexError:
            raise SensorPolling("Attempted to fetch data too quickly")

    def read_iaq(self):
        """Calculate an IAQ score 0-100%, returns a float"""

        # 40% is deemed a good indoor quality baseline for humidity
        humidity_baseline = 40
        # Defines how much weight humidity should play in air quality
        humidity_weighting = 0.25

        # Read the sensor once to get humidity and raw gas values
        reading_1 = self._get_iaq_data()
        gas_resistance_reading = reading_1[0]
        humidity_reading = reading_1[1]

        #  How far is the reading_1 humidity off from the baseline humidity
        humidity_offset = humidity_reading - humidity_baseline

        # From the above humidity offset,
        # we could end up with a positive or negative
        # we need to handle the math to score a positive
        # value and negative value different
        if humidity_offset > 0:
            humidity_score = (100 - humidity_baseline - humidity_offset) / \
                             (100 - humidity_baseline) * \
                              (humidity_weighting * 100)
        else:
            humidity_score = (humidity_baseline + humidity_offset) / \
                             humidity_baseline * (humidity_weighting * 100)

        # BME60 gas sensor has a refresh of 1s
        sleep(1)
        # Take another reading of the gas
        reading_2 = self._get_iaq_data()
        gas_resistance_reading_2 = reading_2[0]

        # Work out the offset between our two gas readings
        gas_offset = gas_resistance_reading - gas_resistance_reading_2

        # From the above gas offset, we could end up with positive or negative
        # same logic as the humidity score
        if gas_offset > 0:
            gas_score = (gas_resistance_reading_2 / gas_resistance_reading) * \
                        (100 - (humidity_weighting * 100))
        else:
            gas_score = 100 - (humidity_weighting * 100)

        # add the scores together , max of 100
        # 100 is perfect
        # 0 is your dead
        iaq_percent = humidity_score + gas_score
        return (iaq_percent)
