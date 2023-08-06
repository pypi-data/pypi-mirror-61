# ARBD1 Library

Library for controlling ARBD1 On Board sensors and actuators of ARBD1.<br/>
About ARBD1 - <a href="about_arbd1.md">about_arbd1</a><br/>
ARBD1 Documentation - https://arbd1.hatchnhack.com/<br/>
Buy Link - https://www.hnhcart.com/products/arbd-1

## Installing Arbd1 Library and uploading firmata firmware to Arbd1

Some text

## Creating Object of Arbd1
    from Arbd import arbd1
    board=Arbd1(COM)
    # accepts string values for COM PORT 
    # e.g. board=Arbd1('COM3')
    
    
## Available Methods
    potentiometer()
    # Returns the value of on board potentiometer.
    # Returned value range is from 0.00 to 1.00
    
    rgb_digital(r,g,b)  
    # Used to control RGB lights on ARBD1
    # r,g,b are boolean values, argument is either 1 or 0
    
    rgb_analog(r,g,b)
    # Used to control RGB lights on ARBD1 with varying intensity
    # r,g,b are float values, its range from 0.00 to 1.00
    
    navigation_switches()
    # Return Values depending on the button pressed on Navi Switch
    ''' 
    Return Values:
    1 (Up Pressed),      
    2 (Down Pressed),   
    3 (Left Pressed),       
    4 (Right Pressed),      
    5 (Center Pressed).  
    0 (Nothing Pressed).
    '''
    
    ldr()
    # Returns the value of on board ldr sensor.
    # Returned value range is from 0.00 to 1.00
    
    buzzer(x)
    # turns on the buzzer of ARBD1
    # 0.0 <= x <= 1.0
    # 0 for least intensity and 1 for highest intensity 
    
    temp_and_humidity() 
    # Returns List of integers
    # 0th index is temperature(in degree celcius)
    # 1st index is humidity(in percentage)
    
    charlieplexing(a1,a2,a3)  
    # Function used to control charlieplexed LED's on ARBD1
    # More details on charlieplexing- https://arbd1.hatchnhack.com/arbd1-peripherals/multiplexing/charlieplexing
     '''
     accepts characters as argument :
    'Z' - HIGH IMPEDENCE
    'H' - HIGH
    'L' - LOW
     '''
     charlieplexing_pov()
     # creates persistence of vision, that all charliplexed led's are on
     # WARNING - program goes to infinite loop
     
 ## Available Variables
     #Used to produce delays because sometimes it is not possible to get values instantly from ARBD1
     potentiometer_delay         
     ldr_delay              
     dht_delay                 
     navigation_switches_delay
     
 ## Examples
 
Printing Pressed Navigation Switch 

     from Arbd import arbd1
     
     board=Arbd1('COM3')
     board.navigation_switches_delay=1
     while 1:
        value=board.navigation_switches()
        if value==1:
          print('UP Pressed')
        elif value==2:
          print('DOWN Pressed')
        elif value==3:            
          print('LEFT Pressed')
        elif value==4:            
          print('RIGHT Pressed') 
        elif value==5:            
          print('CENTER Pressed') 

Turning On and Off Red RGB Led

    from Arbd import arbd1
    
    board=Arbd1('COM3')
    board.rgb_digital(1,0,0)
    time.sleep(1)
    board.rgb_digital(0,0,0)
 
 Printing ldr values
 
    from Arbd import arbd1
    
    board=Arbd1('COM3')
    while 1:
      print(board.ldr())
 
 Getting Real Time Potentiometer Values
     
    from Arbd import arbd1
    
    board=Arbd1('COM3')
    while 1:
      print(board.potentiometer()) 
 Getting Temperature and Humidity Values 
 
    from Arbd import arbd1
    
    board=Arbd1('COM3')
    while 1:
      time.sleep(1)
      temp_humd=board.temp_and_humidity()
      print('Temperature is ',temp_humd[0], 'Celsius')
      print('Humidity is ', temp_humd[1], 'Percentage')
      
  Turning On and Off Buzzer

    from Arbd import arbd1
    
    board=Arbd1('COM3')
    board.buzzer(1)
    time.sleep(1)
    board.buzzer(0)
    
  Using Charlieplexing
  
    from Arbd import arbd1
    
    board=Arbd1('COM3')
    board.charlieplexing('Z','Z','L','H') # turns on 1st LED
    time.sleep(1)
    board.charlieplexing('H','L','Z','Z') # turns on 12th LED
    

   
  
