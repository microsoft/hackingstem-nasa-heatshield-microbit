# ------------__ Hacking STEM – heat_shield.py – micro:bit __-----------
#  For use with the TODO: Lesson title
#  lesson plan available from Microsoft Education Workshop at
#  http://aka.ms/hackingSTEM
#
#  Overview: This project reads the resistance of 2 thermistors and converts
#  that value to temprature using the stienhart-hart formula. Each of the
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
DATA_RATE = 1000  # Frequency of code looping
EOL = '\n'  # End of Line Character

# Pins where the Thermistors are connected
material_therm_pin = pin0
hair_dryer_therm_pin = pin1


def get_resistance(pin):
    # TODO: remove sampling code
    # num_samples = 5
    # samples = []
    # average = 0

    # for i in range(num_samples):
    #     samples.append(pin.read_analog())
    #     sleep(10)

    # for i in range(num_samples):
    #     average += samples[i-1]

    # average /= num_samples

    series_resistor = 10000

    READING = pin.read_analog()
    VOLTAGE = 1023 / READING - 1
    RESISTANCE = series_resistor / VOLTAGE
    return (RESISTANCE)


def stienhart(resistance):
    # Thermistor Resistance at 25 c
    therm_nominal = 10000.0
    # temperature for nominal resistance
    temp_nominal = 25.0
    # Beta coefficient of the thermistor (this avialable in the data sheet)
    beta_co = 3950.0
    # The rest of this is a fairly complex formula
    temperature = resistance/therm_nominal
    temperature = math.log(temperature)
    temperature /= beta_co
    temperature += 1.0 / (temp_nominal + 273.15)
    temperature = 1.0 / temperature
    temperature -= 273.15
    return temperature


# =========================================================================== #
# --------------The Code Below Here is for Excel Communication--------------- #
# =========================================================================== #

# Array to hold the serial data
parsedData = [0] * 5


def getData():
    # This function gets data from serial and builds it into a string
    # it is farily specialized, don't worry if you don't understand it
    global parsedData, builtString
    builtString = ""
    while uart.any() is True:
        byteIn = uart.read(1)
        if byteIn == b'\n':
            continue
        byteIn = str(byteIn)
        splitByte = byteIn.split("'")
        builtString += splitByte[1]
    parseData(builtString)
    return (parsedData)


def parseData(s):
    #   This function seperates the string into an array
    global parsedData
    if s != "":
        parsedData = s.split(",")


while (True):
    # Get the data from serial and store it in a new variable
    serial_in_data = getData()
    # Read the thermistors and convert the resistance value to temprature
    material_temprature = stienhart(get_resistance(material_therm_pin))
    hair_dryer_temprature = stienhart(get_resistance(hair_dryer_therm_pin))
    # Check if pause command was sent
    if (serial_in_data[0] != "#pause"):
        # uart is the micro:bit command for serial
        uart.write(',{},{},'.format(material_temprature, hair_dryer_temprature)+EOL)

    sleep(DATA_RATE)
