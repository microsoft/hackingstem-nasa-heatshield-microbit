# ------------__ Hacking STEM – heat_shield.py – micro:bit __-----------
#  For use with the Hacking STEM Heat Shield lesson plan available from 
#  Microsoft Education Workshop at http://aka.ms/hackingSTEM
#
#  Overview: This project reads the resistance of two thermistors and converts
#  that value to temperature using the stienhart-hart formula. Each of the
#  thermistors is setup with a voltage divider, so that we can use the voltage
#  divider equation to accurately measure the resistance.
#
#  This project uses a BBC micro:bit microcontroller, information at:
#  https://microbit.org/
#
#  Comments, contributions, suggestions, bug reports, and feature
#  requests are welcome! For source code and bug reports see:
#  http://github.com/[TODO github path to Hacking STEM]
#
#  Copyright 2019, Adi Azulay
#  Microsoft EDU Workshop - HackingSTEM
#  MIT License terms detailed in LICENSE.txt
# ===---------------------------------------------------------------===

from microbit import *
import math

# Setup & Config
display.off()  # Turns off LEDs to free up additional input pins
uart.init(baudrate=9600)  # Sets serial baud rate
DATA_RATE = 1000  # Frequency of code looping in milliseconds
EOL = '\n'  # End of Line Character

# Pins where the Thermistors are connected
MATERIAL_THERM_PIN = pin0
HAIR_DRYER_THERM_PIN = pin1


def get_resistance(pin):
    SERIES_RESISTOR = 10000

    reading = pin.read_analog()
    voltage = 1023 / reading - 1
    resistance = SERIES_RESISTOR / voltage
    return (resistance)


def stienhart(resistance):
    # Thermistor Resistance at 25 c
    THERM_NOMINAL = 10000.0
    # temperature for nominal resistance
    TEMP_NOMINAL = 25.0
    # Beta coefficient of the thermistor (this avialable in the data sheet)
    BETA_CO = 3950.0
    # The rest of this is a fairly complex formula
    value = resistance/THERM_NOMINAL
    value = math.log(value)
    value /= BETA_CO
    value += 1.0 / (TEMP_NOMINAL + 273.15)
    value = 1.0 / value
    value -= 273.15
    temperature = value
    return temperature

while (True):
    # Read the thermistors and convert the resistance value to temprature
    material_temprature = stienhart(get_resistance(MATERIAL_THERM_PIN))
    hair_dryer_temprature = stienhart(get_resistance(HAIR_DRYER_THERM_PIN))
    # uart is the micro:bit command for serial
    uart.write('{},{},'.format(material_temprature, hair_dryer_temprature)+EOL)

    sleep(DATA_RATE)
