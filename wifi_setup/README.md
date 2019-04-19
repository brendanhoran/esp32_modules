## Wrapper libary to set up a basic wifi network connection

# Overview
A wrapper to help easily set up wifi connections in micropython.   
All methods will raise exceptions on errors.   

The wifi_setup() method takes two arguments, SSID name and password.  
The wifi(setup.connect(), will attempt to connect to the above network.  
Once connected it will print the IP address it has received.  
If there has been an issue it will stop retrying to connect and raise an exception.   



# Usage :

```
import wifi_setup
wifi_setup = wifi_setup.WIFI_setup('SSID','PASSWORD')
wifi_setup.connect()
```

