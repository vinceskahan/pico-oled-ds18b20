# PCD8544 (Nokia 5110) LCD sample for Raspberry Pi Pico
# Required library:
# https://github.com/mcauser/micropython-pcd8544

# Connections:
#   Connect the screen up as shown below using the
#   physical pins indicated (physical pin on pico)

#   RST - Reset:                     Pico GP8 (11)     
#   CE - Chip Enable / Chip select : Pico GP5 ( 7)     
#   DC - Data/Command :              Pico GP4 ( 6)     
#   Din - Serial Input (Mosi):       Pico GP7 (10)
#   Clk - SPI Clock:                 Pico GP6 ( 9)
#   Vcc:                             Pico 3V3 (36)
#   BL :                             Pico GP9(12)
#   Gnd:                             Pico GND (38)
#
#----- add the ds18b20 as well ----
#
# (curved side of sensor)
#    Gnd Data VCC
#
# with Data connected to Pico GPIO17 (22)
#


import pcd8544_fb
from machine import Pin, SPI
import utime

import machine, onewire, ds18x20, time

# set up pins

spi = SPI(0)
spi.init(baudrate=2000000, polarity=0, phase=0)
cs = Pin(5)
dc = Pin(4)
rst = Pin(8)

ds_pin = Pin(17) 
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

# set bl off
back_light = Pin(9, Pin.OUT, value=1)

#initialize lcd
lcd = pcd8544_fb.PCD8544_FB(spi, cs, dc, rst)

# Setup temperature sensor read value on ADC 4 - Onboard temperature sensor
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

def display_ds_temp(string_ds_temperature):
    lcd.text('Current temp degF', 0, 0, 1)
    lcd.text(string_ds_temperature,0,12,1)
    lcd.clear()
    lcd.show()
    utime.sleep(5)

def display_temp(string_temperature):
    # refresh occasionally to show program is running
    lcd.clear()
    lcd.show()
    utime.sleep(1)
    lcd.text(string_temperature,15, 20, 1)
    lcd.show()
    utime.sleep(5)

def read_ds_temp():
    roms = ds_sensor.scan()
    if roms:
        try:
            ds_sensor.convert_temp()
            time.sleep_ms(750)
            for rom in roms: 
                # print(rom)
                temp = ds_sensor.read_temp(rom)*1.80+32
                temp_formatted = str("{:.1f}".format(temp) + " F")
                print(temp_formatted)
        except:
            temp_formatted = "   unavailable"
    return(temp_formatted)
    
  
def read_temp():
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    formatted_temperature = "{:.2f}".format(temperature)
    string_temperature = str("Temp:" + formatted_temperature)
    print(string_temperature)
    
    return string_temperature
    


while True:
    #    temperature = read_temp()
    temperature = read_ds_temp()
    display_temp(temperature)
    lcd.fill(0)
 
