## Wrapper library for the BME680 sensor made by DF-Robot       

# Overview        
This simple library aims to wrap up all the basic functions into easy to use methods.   
All methods will raise exceptions on any errors.    
Also supports a custom method to calculate [IAQ](https://en.wikipedia.org/wiki/Indoor_air_quality).   
Will return a IAQ score from 0-100.    
Where 0 is most likely going to kill you and 100% is the best IAQ given the sensors resolution.   
This wrapper is tested with the [DF-Robot bme680 board](https://www.dfrobot.com/product-1697.html).   
However it should support any bme680 sensor board with no issues.    

Take note that the above sensor is hardwired to I2C address : 0x77.   

For the DF-Robot sensor, this library depends on my modified bme680 base library, [df-robot-bme680-micropython](https://gitlab.com/brendanhoran/df-robot-bme680-micropython).  


# Usage:    

```
sensor = bme680_wrapper.BME680_sensor(22,21)
sensor.read_temperature()
sensor.read_humidity()
sensor.read_pressure()
sensor.read_gas_resistance()
sensor.read_iaq()
```     

Where "sensor = bme680_wrapper.BME680_sensor(22,21)" pins are SCL and SDA.    

Also see the pydoc strings in [bme680_wrapper.py](https://gitlab.com/brendanhoran/esp32_modules/blob/master/bme680/bme680_wrapper.py).   
