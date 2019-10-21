#!/usr/bin/env python
from lib.Bcolors import Bcolors
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.commands_chip as chip
import time

def chip_setup():
	#Setup read and write port
    writePort = WritePort("/dev/xillybus_write_32",32)
    readPort  = ReadPort("/dev/xillybus_read_32",32)

    if not writePort.openPort():
        print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)
        quit()

    if not readPort.openPort():
        print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)

    real_freq = chip.set_clock(100, writePort)
    print("Real freq: " + str(real_freq))

    time.sleep(2.5)

    chip.start(writePort)


    # Send a program to the chip
    chip.reset(readPort, writePort)

    # Close ports
    writePort.closePort()
    readPort.closePort()

    return

chip_setup()
