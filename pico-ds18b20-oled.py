#----------------------------------------------------
#
# original git checkin - 2022-07-12
#
# quickie pi pico program to display temperatures
# from one or more DS18b20 sensors on a OLED display
#   - tested with two sensors
#
# this will print to the Thonny console as well
# when run that way
#
# wiring setup:
#
# sensors:
#    with DS18b20 flat side facing you, pins are GND DATA VCC
#       and put a 10k resistor across DATA and VCC
#    other sensors can be put on the same rows on the breadboard
#    ala:
#
#       GND       DATA          VCC
#        X----------X------------X
#        |          |            |
#        |          |    4.7k    |
#        |          |--resistor--|
#        |          |            |
#              (to sensor)
#              (to sensor)
#
# on the pico:
#    GPIO0     pin  1 to SDA on the OLED
#    GPIO1     pin  2 to SCL on the OLED
#    GPIO4     pin  6 to data on the DS18b20(s)
#    3V3i(OUT) pin 37 to 3.3V power rail
#    GND       pin 38 to ground rail
#
# on the I2C OLED:
#    VCC to 3.3V power rail
#    GND to ground rail
#    SCL to GPIO1 pin 2 on the pico
#    SDA to GPIO0 pin 1 on the pico
#
# credits:
#    - this is based on a bunch of howto pages on Internet
#      which all seem to be copying each other, so I can't tell
#      who the original demo author actually is
#
# to-do:
#    - this needs a lot of try/except hardening
#----------------------------------------------------
       
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

import machine,onewire,ds18x20,time
ds_pin = machine.Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

i2c=I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

def displayTemp(temp,line):
    oled.text("Degrees F", 0, 0)
    oled.text(temp, 0, line)
    oled.show()

def printTemps():
    roms = ds_sensor.scan()
    #print('Found DS devices: ',roms)
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    romNum=10
    oled.fill(0)
    oled.show()
    for rom in roms:
        tempF=(ds_sensor.read_temp(rom) * 1.8 + 32)

        print(tempF)

        line=romNum+10
        displayTemp(str(tempF),line)
        romNum = romNum+10

    time.sleep(5)
    print("-----")

while True:
    printTemps()
