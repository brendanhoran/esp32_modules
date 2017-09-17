
REF:    
https://www.dfrobot.com/wiki/index.php/Gravity:_Analog_Infrared_CO2_Sensor_For_Arduino_SKU:_SEN0219    
https://www.futurlec.com/Datasheet/Sensor/MH-Z14.pdf   

Usage:   

```
import c02
c02 = c02.C02_sensor(36)
c02.read_sensor()
```

Where 36 is the pin the C02 Sensor is connected to. Must be an ADC pin.


