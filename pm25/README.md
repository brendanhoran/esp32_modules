## Library for the DF-Robot pm2.5 serial laser dust sensor

# Overview
A micropython library for the DF-Robot serial laser dust sensor.        
All methods will raise exceptions on errors.       

The read_sensor() method will return 3 dust level readings.       
pm 1.0, pm 2.5 , pm 10 . All readings are in ug/m3.    
Sensor range : Measuring Range: 0 - 1000 ug/m3.     


# References:     
[DF-Robot sensor](https://www.dfrobot.com/product-1272.html)    
[DF-Robot wiki page](https://www.dfrobot.com/wiki/index.php/PM2.5_laser_dust_sensor_SKU:SEN0177)    
[Datasheet](https://github.com/Arduinolibrary/DFRobot_PM2.5_Sensor_module/raw/master/HK-A5%20Laser%20PM2.5%20Sensor%20V1.0.pdf)   

# Usage :   

```
import pm25
pm25 = pm25.PM25_sensor(25,26)
pm25.read_sensor()
```

Where 25 is the TX pin of the PM25 and 26 is the RX pin of the PM25.    
This code will create a new UART from any two digial pins.   
