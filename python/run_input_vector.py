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

# Set clock frequency
real_freq = chip.set_clock(10, writePort)
print("Real freq: " + str(real_freq))

# Reset chip
chip.reset(readPort, writePort)


time.sleep(0.5)

# Send a program to the chip
print("Sending data to RAM")
chip.enable_write_mode(writePort)
vector = '../input_vectors/input_vector_C1.in'
with open(vector) as fp:
   line = fp.readline()
   while line:
       print("Vector instruction: {}".format(line.strip()))
       instr = re.split(' |; |, |\*|\t',line)

       addr = (int(instr[0][0:4], 16))
       value = (int(instr[1][0:4], 16))
       chip.write_to_mem(addr, value, writePort)
       line = fp.readline()

#input("Press Enter to continue...")
chip.enable_exit_mode(writePort)
#input("Change clock and press Enter to continue...")

time.sleep(0.5)

chip.start(writePort)

time.sleep(5)


now = datetime.now()
date_time = now.strftime("%m%d-%H%M%S")
filename = "../results/" + str(date_time) + "_spi-results.txt"
chip.readout_memory(readPort, writePort, 0, 7, const.WR_MEMORY, filename)


# Close ports
writePort.closePort()
readPort.closePort()
