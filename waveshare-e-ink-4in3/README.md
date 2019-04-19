## Library for the Waveshare 4.3" e-ink UART display    

# Overview
A easy to use library to communicate with the e-ink display.     
Currently supports writing text, setting font size, and some auxiliary functions.    
All methods will raise exceptions on errors.     


# References :    
[Df-Robot 4.3" e-ink display](https://www.dfrobot.com/product-1312.html)       
[Waveshare wiki page](https://www.waveshare.com/wiki/4.3inch_e-Paper_UART_Module)     
[Manual/data sheet for the display](https://www.waveshare.com/wiki/File:4.3inch-e-Paper-UserManual.pdf)    



# Usage :       

**Set up the display:**     
```
import eink
eink = eink.EINK_display(25,26)
eink.hand_shake()
```

Where 25 is the "DOUT/4" pin on the display and 26 is the "DIN/3" pin on the display.   
The hand_shake() method will return "OK" if the handshake process was successful, otherwise an exception will be raised.    

**Write text to the display via line number:**    

```
eink.write_line("large_text_line_example", "large", 1)
```

The write_line() method takes three arguments:
 * string -- Text string to write to the display
 * font size -- size of the font to use (small, medium, large)
 * line number - vertical line number to write text to, max 10, 13, 21
 
The method will not return anything on success. Exception will be raised if the arguments are malformed.     
*NOTE:* The write_line() method will not clear the display. This enables you to add text with additional calls of the write_line() method.    

You can mix font sizes on the same write/refresh cycle of the display.   

This method is the preferred way to write text to the display.   


**Write some text to the display via X,Y coordinates:**    
```
eink.write_string("brr", 10, 10)
```

The write_string() method takes three arguments:
* string -- Text string to write to the display
* x_pos -- X position of the start of the string
* y_pos -- Y position of the start of the string

The method will not return anything on success. Exception will be raised if the arguments are malformed.     
*NOTE:* The write_string() command will not clear the display. This enables you to add text with additional calls of the write_string() method.    

**Clear the display:**
```
eink.clear_display()
```

The clear_display() method takes no arguments.      
This will clear the display of everything.      
Will raise an exception if the display rejects the commands, otherwise returns nothing.    

**Set font size:**      
```
eink.set_font_size(64)
```


The set_font_size(** method takes one argument:      
* size -- font size ,32,48,64     

The method will not return anything on success. Exception will be raised if you specify an invalid size.   

**Get the currently set font size**    
```
eink.get_font_size()
```

The get_font_size() method takes no arguments.   
Will return the English name of the currently set font size.    
