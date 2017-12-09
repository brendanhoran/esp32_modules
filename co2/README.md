*Work in progress*

REF:    
https://www.dfrobot.com/wiki/index.php/Gravity:_Analog_Infrared_CO2_Sensor_For_Arduino_SKU:_SEN0219    
https://www.futurlec.com/Datasheet/Sensor/MH-Z14.pdf   

Usage:   

```
import co2
co2 = co2.CO2_sensor(36)
co2.read_sensor()
```

Where 36 is the pin the co2 Sensor is connected to. Must be an ADC pin.


