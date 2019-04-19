## Library for the DF-Robot Infrared Co2 Sensor     


# Overview   

A micropython library for the DF-Robot Infrared Co2 sensor.   
All methods will raise exceptions on errors.     

The read_sensor() method will return a Co2 reading in ppm(parts per million).   
Sensor range : Measuring Range: 0 - 5000 ppm

# References:       
[DF-Robot sensor board](https://www.dfrobot.com/product-1549.html)   
[DF-Robot wiki page](https://www.dfrobot.com/wiki/index.php/Gravity:_Analog_Infrared_CO2_Sensor_For_Arduino_SKU:_SEN0219)   
[Sensor data sheet](https://www.futurlec.com/Datasheet/Sensor/MH-Z14.pdf)     

# Usage:   

```
import co2
co2 = co2.CO2_sensor(36)
co2.read_sensor()
```

Where 36 is the pin the Co2 Sensor is connected to. Must be an ADC pin.    

