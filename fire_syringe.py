# ------------__ Hacking STEM – heat_shield.py – micro:bit __-----------
# For use with the TODO Lesson plan
# available from Microsoft Education Workshop at
# https://aka.ms/heatshield
# http://aka.ms/hackingSTEM
#
#  Overview:
#  This project uses two TMP 36 temperature sensors:
#    TMP36 temperature sensor input on pin 0
#    TMP36 temperature sensor input on pin 1
#
#  example: TODO
#
#  This project uses a BBC micro:bit microcontroller, information at:
#  https://microbit.org/
#
#  Comments, contributions, suggestions, bug reports, and feature
#  requests are welcome! For source code and bug reports see:
#  http://github.com/[TODO github path to Hacking STEM]
#
#  Copyright 2019, Jeremy Franklin-Ross
#  Microsoft EDU Workshop - HackingSTEM
#  MIT License terms detailed in LICENSE.txt
# ===---------------------------------------------------------------===

from microbit import *

TMP36_EXTERNAL_PIN = pin0

TMD36_OFFSET = 0.56     # Offset for temperature application
ADC_RESOLUTION = 1024   # analoge to digital scale
MICROBIT_VOLTAGE = 3.3  # voltage for circuit calculations


# End of line string
EOL = "\n"


def read_temp(pin):
    """ Reads temperature from sensor """
    sensorInput = pin.read_analog()
    volts = (sensorInput/ADC_RESOLUTION) * MICROBIT_VOLTAGE
    celcius = (volts - TMD36_OFFSET) * 100

    return celcius

# Set up & config
uart.init(baudrate=9600) # set serial data rate


#send zeros to begin session
uart.write(EOL+"INIT,0"+EOL)


while True:
    external_celcius = read_temp(TMP36_EXTERNAL_PIN)
    uart.write("{},{}".format("",external_celcius)+EOL)
    #TODO implement moving average with 10 milli reads and 100 millis writes
    sleep(10) 

