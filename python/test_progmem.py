#!/usr/bin/env python
from lib.Bcolors import Bcolors
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
from lib.programmer import ProgMem
import lib.commands_chip as chip
import lib.constants as const
from datetime import datetime
import time
import re

#Setup read and write port
writePort = WritePort("/dev/xillybus_write_32",32)
readPort  = ReadPort("/dev/xillybus_read_32",32)
programmer = ProgMem("../input_vectors/input_vector_C0.in")

if not writePort.openPort():
    print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)
    quit()
if not readPort.openPort():
    print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)


addr, val = programmer.readWord()
print("{:04x}".format(addr) + " " + "{:04x}".format(val))

addr, val = programmer.readWord()
print("{:04x}".format(addr) + " " + "{:04x}".format(val))

addr, val = programmer.readWord()
print("{:04x}".format(addr) + " " + "{:04x}".format(val))

addr, val = programmer.readWord()
print("{:04x}".format(addr) + " " + "{:04x}".format(val))

addr, val = programmer.readWord()
print("{:04x}".format(addr) + " " + "{:04x}".format(val))

programmer.setAddress(0);

addr, val = programmer.readWord()
print("{:04x}".format(addr) + " " + "{:04x}".format(val))

addr, val = programmer.readWord()
print("{:04x}".format(addr) + " " + "{:04x}".format(val))

addr, val = programmer.readWord()
print("{:04x}".format(addr) + " " + "{:04x}".format(val))

addr, val = programmer.readWord()
print("{:04x}".format(addr) + " " + "{:04x}".format(val))

addr, val = programmer.readWord()
print("{:04x}".format(addr) + " " + "{:04x}".format(val))

chip.reset(readPort, writePort)

# Set the clock frequency
real_freq = chip.set_clock(10, writePort)
print("Real freq: " + str(real_freq))

time.sleep(0.5)

chip.write_mem(42, writePort)

#
# # Send a program to the chip
# chip.reset(readPort, writePort)
#
# #time.sleep(0.5)
#
# print("Sending data to RAM")
# # Set the clock frequency
# real_freq = chip.set_clock(100, writePort)
# print("Real freq: " + str(real_freq))

# Close ports
writePort.closePort()
readPort.closePort()
