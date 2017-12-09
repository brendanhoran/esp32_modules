*work in progress*

REF :     
https://www.dfrobot.com/wiki/index.php/PM2.5_laser_dust_sensor_SKU:SEN0177    
https://github.com/Arduinolibrary/DFRobot_PM2.5_Sensor_module/raw/master/HK-A5%20Laser%20PM2.5%20Sensor%20V1.0.pdf    

Usage :   

```
import pm25
pm25 = pm25.PM25_sensor(25,26)
pm25.read_sensor()
```

Where 25 is the TX pin of the PM25 and 26 is the RX pin of the PM25.    
This code will create a new UART from any two digial pins.   
