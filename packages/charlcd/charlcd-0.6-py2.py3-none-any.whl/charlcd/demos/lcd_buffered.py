#!/usr/bin/python
# -*- coding: utf-8 -*-
"""test script for buffered lcd"""

import sys
sys.path.append("../../")
import RPi.GPIO as GPIO  # NOQA pylint: disable=I0011,F0401
from charlcd import buffered as lcd  # NOQA
from charlcd.drivers.gpio import Gpio  # NOQA
from charlcd.drivers.i2c import I2C  # NOQA

GPIO.setmode(GPIO.BCM)


def test1():
    """demo 20x4 and 16x2"""
    lcd_2 = lcd.CharLCD(20, 4, Gpio())
    lcd_2.init()
    lcd_2.write('-  Blarg !')
    lcd_2.write('-   Grarg !', 0, 1)
    lcd_2.write('-    ALIVE  !!!!', 0, 2)

    lcd_2.flush()

    lcd_2.write('-    ALIVE  !!!!.', 0, 2)
    lcd_2.flush()

    # lcd_1 = lcd.CharLCD(16, 2, I2C(0x20, 1), 0, 0)
    # lcd_1.init()
    # lcd_1.write('-!Second blarg!')
    # lcd_1.write("-second line", 0, 1)
    # lcd_1.flush()


def test2():
    """demo 40x4"""
    drv = Gpio()
    drv.pins['E2'] = 10
    drv.pins['E'] = 24
    lcd_1 = lcd.CharLCD(40, 4, drv, 0, 0)
    lcd_1.init()
    lcd_1.write('-  Blarg !')
    lcd_1.write('-   Grarg !', 0, 1)
    lcd_1.write('-    ALIVE  !!!!', 0, 2)
    lcd_1.flush()

    lcd_1.write('/* ', 19, 0)
    lcd_1.write('|*|', 19, 1)
    lcd_1.write(' */', 19, 2)

    lcd_1.flush()


def test3():
    """demo 16x2"""
    lcd_1 = lcd.CharLCD(16, 2, I2C(0x20, 1), 0, 0)
    lcd_1.init()
    lcd_1.set_xy(10, 0)
    lcd_1.stream("1234567890qwertyuiopasdfghjkl")
    lcd_1.flush()


def test4():
    """demo 2 screens via i2c"""
    i2c_20x4 = I2C(0x3b, 1)
    #i2c_16x2 = I2C(0x25, 1)

    i2c_20x4.pins = {
        'RS': 6,
        'E': 4,
        'E2': None,
        'DB4': 0,
        'DB5': 1,
        'DB6': 2,
        'DB7': 3
    }
    # i2c_16x2.pins = {
    #     'RS': 6,
    #     'E': 4,
    #     'E2': None,
    #     'DB4': 0,
    #     'DB5': 1,
    #     'DB6': 2,
    #     'DB7': 3
    # }
    lcd_1 = lcd.CharLCD(20, 4, i2c_20x4)
    lcd_1.init()
    lcd_1.set_xy(0, 0)
    lcd_1.stream("Kab00m")
    lcd_1.flush()

    lcd_1.write('siemka', 10, 3)
    lcd_1.flush(True)
    lcd_1.shutdown()
    # lcd_2 = lcd.CharLCD(16, 2, i2c_16x2)
    # lcd_2.init()
    # lcd_2.set_xy(0, 0)
    # lcd_2.stream("1")
    # lcd_2.flush()


def test5():
    """demo 2 screens via i2c"""
    i2c_20x4 = I2C(0x3b, 1)
    #i2c_16x2 = I2C(0x25, 1)

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
    lcd_1.add_custom_char(0, [
        0x04, 0x0e, 0x0e, 0x0e, 0x0e, 0x1f, 0x04, 0x04
    ])
    lcd_1.add_custom_char(1, [
        0b00011, 0b00100, 0b11110, 0b01000, 0b11110, 0b01000, 0b00111
    ])
    lcd_1.add_custom_char(2, [
        0b00000,
        0b00000,
        0b00000,
        0b01010,
        0b00000,
        0b00100,
        0b10001,
        0b01110
    ])
    lcd_1.set_xy(0, 0)
    lcd_1.stream("Kab00m")
    lcd_1.stream(chr(0x00))
    lcd_1.stream(chr(0x01))
    lcd_1.write(chr(0x02), 9, 2)
    lcd_1.flush()
    # lcd_1.shutdown()


test5()