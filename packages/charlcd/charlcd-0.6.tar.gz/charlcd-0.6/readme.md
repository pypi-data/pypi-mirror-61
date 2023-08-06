What it is
===

Pack of HD44780 lcd drivers to be used with Raspberry PI. 
It gives functions to quickly control what is displayed and how.
Supports i2c, GPIO wiring and WiFi remote LCD. 

Use two modes:

- direct - write to lcd asap
- buffered - write to buffer and do flush 

Supports virtual lcds - ability to join few lcd into one

Supports 20x4, 16x2, 40x4 and so.

Include simple game Piader that utilize vlcds - demo

See more: [koscis.wordpress.com](https://koscis.wordpress.com)

Content
===

## LCDs

Class direct.
Supports displaying chars on lcd. Using direct mode, means each char is displayed 
as soon as possible.

Class buffered.
Use buffer to set what need to be displayed and flush function to draw on screen.
Its drawing only those chars that differ from last frame.

Class virtual_direct.
Allows to set virtual lcd. Rect area on any number of lcds. Uses direct mode

Class virtual_buffered.
Allows to set virtual lcd. Rect area on any number of lcds. Uses buffered mode
 
## Drivers

###GPIO driver
Driver that use GPIO pins as connection to lcd. Default pins:

    LCD : GPIO
    RS  : 24
    E   : 17
    E2  : None
    DB4 : 27
    DB5 : 25
    DB6 : 23
    DB7 : 22

To use 40x4 lcd set E2

###I2C driver
Use i2c bus to control lcd. Default connection:

    GPIO :  PCF8574
    GND  :  A0
    GND  :  A1
    GND  :  A2
    GND  :  GND
    +5V  :  Vcc
    SDA  :  SDA
    SCL  :  SCL
    
    PCF8574  :   LCD
    P4       :   LCD4 (RS)
    P5       :   LCD6 (E)
    P3       :   LCD14 (DB7)
    P2       :   LCD13 (DB6)
    P1       :   LCD12 (DB5)
    P0       :   LCD11 (DB4)


###WiFi direct driver
This one use UDP broadcast to transmit each command/char to remote LCD
[See here for NodeMCU remote LCD](https://github.com/bkosciow/nodemcu_boilerplate)
[Articles](https://koscis.wordpress.com/tag/nodehd44780/)   

###WiFi content driver
Sends UDP message with full content to remote LCD.
[See here for NodeMCU remote LCD](https://github.com/bkosciow/nodemcu_boilerplate)
[Articles](https://koscis.wordpress.com/tag/nodehd44780/)   


###Null and NullEvents driver
Used in tests


Wiring
===

## GPIO 40x4

    LCD13 [VSS] ------------ GND
    LCD14 [VDD] ------------ +5V
    LCD12 [V0] ------/\/\/\ [potentiometer]
                       \---- GND
    LCD11 [RS] ------------- GPIO 25
    LCD10 [R/W] ------------ GND
    LCD9  [E1] ------------- GPIO 24
    LCD15 [E2] ------------- GPIO 10
    LCD4  [DB4] ------------ GPIO 22
    LCD3  [DB5] ------------ GPIO 23
    LCD2  [DB6] ------------ GPIO 27
    LCD1  [DB7] ------------ GPIO 17
    LCD17 [A] ------/\/\/\ [potentiometer]
                       \---- +5V
    LCD18 [K] -------------- GND

## GPIO 20x4, 16x2

    LCD1 [VSS] ------------- GND
    LCD2 [VDD] ------------- +5V
    LCD3 [V0] ------/\/\/\ [potentiometer]
                       \---- GND
    LCD4 [RS] -------------- GPIO 25
    LCD5 [R/W] ------------- GND
    LCD6 [E] --------------- GPIO 24
    LCD7 [DB0]
    LCD8 [DB1]
    LCD9 [DB2]
    LCD10 [DB3]
    LCD11 [DB4] ------------ GPIO 22
    LCD12 [DB5] ------------ GPIO 23
    LCD13 [DB6] ------------ GPIO 27
    LCD14 [DB7] ------------ GPIO 17
    LCD15 [A] ------/\/\/\ [potentiometer]
                       \---- +5V
    LCD16 [K] -------------- GND

## I2C 20x4, 16x2

    LCD                                           PCF8574
     1 -------- GND                     GND ----- A0   Vcc ---- +5V 
     2 -------- +5V                     GND ----- A1   SDA ---- SDA on RPi
     3 --/\/\ [potentiometer]           GND ----- A2   SCL ---- SCL on RPi
           \--- GND                   LCD11 ----- P0   INT 
     4 [RS]---- P4                    LCD12 ----- P1   P7
     5 -------- GND                   LCD13 ----- P2   P6
     6 [E]----- P5                    LCD14 ----- P3   P5 ----- LCD6
     7                                  GND ----- GND  P4 ----- LCD4
     8
     9
    10
    11 [DB4]--- P0
    12 [DB5]--- P1
    13 [DB6]--- P2
    14 [DB7]--- P3
    15 --/\/\ [potentiometer]
           \--- +5V
    16 -------- GND

## I2C 40x4

    LCD                                           PCF8574
    13 -------- GND                     GND ----- A0   Vcc ---- +5V 
    14 -------- +5V                     GND ----- A1   SDA ---- SDA on RPi
    12 --/\/\ [potentiometer]           GND ----- A2   SCL ---- SCL on RPi
           \--- GND                    LCD4 ----- P0   INT 
    11 [RS]---- P4                     LCD3 ----- P1   P7
    10 -------- GND                    LCD2 ----- P2   P6 ----- LCD15
     9 [E]----- P5                     LCD1 ----- P3   P5 ----- LCD9
    15 [E2] --- P6                      GND ----- GND  P4 ----- LCD11
     4 [DB4]--- P0
     3 [DB5]--- P1
     2 [DB6]--- P2
     1 [DB7]--- P3
    17 --/\/\ [potentiometer]
           \--- +5V
    18 -------- GND

Usage
===

## GPIO Driver

Simplest way

```
    l = lcd.CharLCD(20, 4, Gpio())
```

Plugin char display 20x4 on GPIO pins. Connections are default.
Custom pins:

    g = Gpio()
    g.pins = {
        'RS': 24,
        'E': 17,
        'E2': None,
        'DB4': 27,
        'DB5': 25,
        'DB6': 23,
        'DB7': 22
    }
    l = lcd.CharLCD(20, 4, g)


Plug 40x4 by GPIO:

    g = Gpio()
    g.pins = {
        'RS': 24,
        'E': 17,
        'E2': 10,
        'DB4': 27,
        'DB5': 25,
        'DB6': 23,
        'DB7': 22
    }
    l = lcd.CharLCD(40, 4, g)

## I2C Driver

```
    l = lcd.CharLCD(16, 2, I2C(0x20, 1))
```

Char display 16x2 on i2c @ 0x20 and bus 1.
To change pins:

    i2c = I2C(0x20, 1)
    i2c.pins = {
        'RS': 4,
        'E': 5,
        'DB4': 0,
        'DB5': 1,
        'DB6': 2,
        'DB7': 3
    }
    l = lcd.CharLCD(16, 2, i2c)


Direct Class
===

Fully working demo (more in demos directory):

    #!/usr/bin/python
    # -*- coding: utf-8 -*-

    """test script for direct lcd input"""

    __author__ = 'Bartosz Kościów'

    import RPi.GPIO as GPIO #pylint: disable=I0011,F0401
    from charlcd import direct as lcd
    from charlcd.drivers.gpio import Gpio
    from charlcd.drivers.i2c import I2C #pylint: disable=I0011,F0401

    GPIO.setmode(GPIO.BCM)

    def test2():
        """demo - 20x4 by gpio"""
        lcd_2 = lcd.CharLCD(20, 4, Gpio())
        lcd_2.init()
        lcd_2.write('-  Blarg !')
        lcd_2.write('-   Grarg !', 0, 1)
        lcd_2.set_xy(0, 2)
        lcd_2.write('-    ALIVE !!!!')
        lcd_2.stream('1234567890qwertyuiopasdfghjkl')

    test2()

### Functions

`CharLCD(width, height, driver, cursor_visible=1, cursor_blink=1)`

`write(self, string, pos_x=None, pos_y=None)` - print string on lcd

`set_xy(pos_x, pos_y)` - move cursor to position

`stream(string)` - stream string, breaks on line ends and after reaching end of display starts from top

Buffered Class
===

Fully working demo (more in demos directory):

    #!/usr/bin/python
    # -*- coding: utf-8 -*-

    """test script for buffered lcd"""

    __author__ = 'Bartosz Kościów'

    import RPi.GPIO as GPIO #pylint: disable=I0011,F0401
    from charlcd import buffered as lcd
    from charlcd.drivers.gpio import Gpio
    from charlcd.drivers.i2c import I2C

    GPIO.setmode(GPIO.BCM)

    def test3():
        """demo 16x2"""
        lcd_1 = lcd.CharLCD(16, 2, I2C(0x20, 1), 0, 0)
        lcd_1.init()
        lcd_1.set_xy(10, 0)
        lcd_1.stream("1234567890qwertyuiopasdfghjkl")
        lcd_1.flush()
    
    
    test3()


###Functions

`CharLCD(width, height, driver, cursor_visible=1, cursor_blink=1)`

`write(content, pos_x=None, pos_y=None)` - writes content into buffer at position(x,y) or current

`set_xy(pos_x, pos_y)` - set cursor position

`get_xy()` - get cursor position

`buffer_clear()` - clears buffer

`flush(redraw_all=False)` - flush buffer to display. With redraw_all=True redraws all chars not only differences

Shared functions
===

`get_width()` - display width

`get_height()` - display height

`get_display_mode()` - return direct or buffered

`shutdown()` - calls driver shutdown

`add_custom_char(pos, bytes)` - adds custom char at pos (0-7). Char is decribed as dict of bytes (see example)

Virtual Direct
===

    #!/usr/bin/python
    # -*- coding: utf-8 -*-
    
    """test script for virtual direct lcd"""
    
    __author__ = 'Bartosz Kościów'
    
    import RPi.GPIO as GPIO #pylint: disable=I0011,F0401
    from charlcd import direct as lcd
    from charlcd.drivers.gpio import Gpio
    from charlcd.drivers.i2c import I2C #pylint: disable=I0011,F0401
    from charlcd import virtual_direct as vlcd
    
    GPIO.setmode(GPIO.BCM)
    
    
    def test2():
        """demo: 16x2 + 20x4 = 36x4 left, right"""
        lcd_1 = lcd.CharLCD(16, 2, I2C(0x20, 1))
        lcd_2 = lcd.CharLCD(20, 4, Gpio(), 0, 0)
        lcd_1.init()
        lcd_2.init()
        vlcd_1 = vlcd.CharLCD(36, 4)
        vlcd_1.add_display(0, 0, lcd_2)
        vlcd_1.add_display(20, 0, lcd_1)
        vlcd_1.write('test me 123456789qwertyuiopasdfghjkl12')
        
    test2()


Virtual Buffered
===

    #!/usr/bin/python
    # -*- coding: utf-8 -*-
    
    """test script for virtual buffered lcd"""
    
    __author__ = 'Bartosz Kościów'
    
    import RPi.GPIO as GPIO #pylint: disable=I0011,F0401
    from charlcd import buffered as lcd
    from charlcd.drivers.gpio import Gpio
    from charlcd.drivers.i2c import I2C
    from charlcd import virtual_buffered as vlcd
    
    GPIO.setmode(GPIO.BCM)
    
    
    def test1():
        """demo: 16x2 + 20x4 = 20x6"""
        lcd_1 = lcd.CharLCD(16, 2, I2C(0x20, 1))
        lcd_2 = lcd.CharLCD(20, 4, Gpio(), 0, 0)
    
        vlcd_1 = vlcd.CharLCD(20, 6)
        vlcd_1.add_display(0, 0, lcd_2)
        vlcd_1.add_display(0, 4, lcd_1)
        vlcd_1.init()
    
        vlcd_1.write('First line')
        vlcd_1.write('Second line', 0, 1)
        vlcd_1.write('Fifth Line', 0, 4)
    
        vlcd_1.set_xy(4, 2)
        vlcd_1.write('third line')
    
        vlcd_1.flush()
    
    test1()


Functions
===
`CharLCD(width, height, driver, cursor_visible=1, cursor_blink=1)` - initialize, lcd size, cursor options

`write(self, string, pos_x=None, pos_y=None)` - print string on lcd

`set_xy(pos_x, pos_y)` - move cursor to position

`get_xy()` - get cursor position

`stream(string)` - stream string, breaks on line ends and after reaching end of display starts from top

`buffer_clear()` - clears buffer (only buffered)

`flush()` - flush buffer to display (only buffered)

`get_width()` - display width

`get_height()` - display height

`get_display_mode()` - return direct or buffered

`shutdown()` - calls driver shutdown

`add_custom_char(pos, bytes)` - adds custom char at pos (0-7). Char is decribed as dict of bytes (see example)


Custom chars - example
===
Works with buffered and direct. Should work with virtual (add char to all displays)

    def test5():
        """demo 2 screens via i2c"""
        i2c_20x4 = I2C(0x3b, 1)
        i2c_20x4.pins = {
            'RS': 6,
            'E': 4,
            'E2': None,
            'DB4': 0,
            'DB5': 1,
            'DB6': 2,
            'DB7': 3
        }

        lcd_1 = lcd.CharLCD(20, 4, i2c_20x4)
        lcd_1.init()
        # lcd_1.set_xy(0, 0)
        lcd_1.add_custom_char(0, [
            0x04, 0x0e, 0x0e, 0x0e, 0x0e, 0x1f, 0x04, 0x04
        ])
        lcd_1.add_custom_char(1, [
            0b00011, 0b00100, 0b11110, 0b01000, 0b11110, 0b01000, 0b00111
        ])
    
        lcd_1.stream("Kab00mek")
        lcd_1.stream(chr(0x01))
        lcd_1.stream(chr(0x00))



test5()


Handler
===
Handler for message_listener package. Supports three events: lcd.cmd, lcd.char and lcd.content.


Demos
===
Check charlcd/demos directory

Piader
===

This game is a simple demo. It show how to utilize any lcd to display a game.

It also shows how to generate a code with 2 fps :)

Controlls:
a - left,
d - right,
space - fire

## How to run:

First lets see a configuration with two lcds. One 20x4 and second 16x2. 
From this two vlcds are made. One 16x6 for game and 4x4 for score. 
 
    #!/usr/bin/python
    # -*- coding: utf-8 -*-
    
    """Game launcher"""
    
    __author__ = 'Bartosz Kościów'
    
    import sys
    sys.path.append("../")
    import RPi.GPIO as GPIO #pylint: disable=I0011,F0401
    from charlcd import buffered
    from charlcd.drivers.gpio import Gpio
    from charlcd.drivers.i2c import I2C
    from charlcd import virtual_buffered
    import piader_1_1.game as game
    
    GPIO.setmode(GPIO.BCM)
    
    
    def main():
        """set lcds and start game"""
        lcd_two = buffered.CharLCD(16, 2, I2C(0x20, 1), 0, 0)
        lcd_one = buffered.CharLCD(20, 4, Gpio(), 0, 0)
    
        vlcd_main = virtual_buffered.CharLCD(16, 6)
        vlcd_main.add_display(0, 0, lcd_one, 4, 0)
        vlcd_main.add_display(0, 4, lcd_two)
        vlcd_main.init()
    
        vlcd_support = virtual_buffered.CharLCD(4, 4)
        vlcd_support.add_display(0, 0, lcd_one)
        vlcd_support.init()
    
        my_game = game.Piader([vlcd_main, vlcd_support])
        my_game.game()
    
    
    main()


Use 40x4 as game lcd:

    drv = I2C(0x3a, 1)
    drv.pins['E2'] = 6
    lcd_three = buffered.CharLCD(40, 4, drv, 0, 0)
    lcd_three.init()
    
    my_game = game.Piader([lcd_three, None])
    
Use 20x4 as game lcd:
    
    lcd_one.init()
    my_game = game.Piader([lcd_one, None])
    

Class diagram
===

    buffered.CharLCD  -->  lcd.CharLCD
                      -->  buffered_interface.Buffered

    direct.CharLCD    -->  lcd.CharLCD
                      -->  direct_interface.Direct

    virtual_buffered.CharLCD  -->  lcd.CharLCDVirtual  -->  lcd.CharLCD
                              -->  buffered_interface.Buffered

    virtual_direct.CharLCD  -->  lcd.CharLCDVirtual  -->  lcd.CharLCD
                            -->  direct.Direct

    gpio.Gpio --\
    i2c.I2C   --->  base.BaseDriver
    null.Null --/