#!/usr/bin/env python
from lib.Bcolors import Bcolors
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.commands_chip as chip
import lib.constants as const
from datetime import datetime
import time
import re

#Setup read and write port
writePort = WritePort("/dev/xillybus_write_32",32)
readPort  = ReadPort("/dev/xillybus_read_32",32)

if not writePort.openPort():
    print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)
    quit()
if not readPort.openPort():
    print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)

# Send a program to the chip
chip.reset(readPort, writePort)

#time.sleep(0.5)

print("Sending data to RAM")
# Set the clock frequency
real_freq = chip.set_clock(25, writePort)
print("Real freq: " + str(real_freq))

# Close ports
writePort.closePort()
readPort.closePort()
