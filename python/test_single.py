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

	chip.start(writePort)

	time.sleep(2.5)

	# Send a program to the chip
	chip.reset(readPort, writePort)
	real_freq = chip.set_clock(10, writePort)
	print("Real freq: " + str(real_freq))

	time.sleep(0.5)


	chip.enable_write_mode(writePort)
	chip.write_to_mem(1, 170, writePort)
	#input("Press Enter to continue...")
	chip.enable_exit_mode(writePort)
	#input("Press Enter to continue...")
	chip.enable_read_mode(0, writePort)
	#input("Press Enter to continue...")
	# i=0
	# while i<2048:
	# 	chip.read_addr(i, writePort)
	# 	i = i+1
	# 	time.sleep(0.1)
	chip.read_addr(1, writePort)
	chip.clear_results(readPort)
	#input("Press Enter to continue...")
	chip.read_addr(1, writePort)
	#input("Press Enter to continue...")
	chip.enable_exit_mode(writePort)

	time.sleep(0.5)
	chip.readout_results(readPort, 100)


	# Close ports
	writePort.closePort()
	readPort.closePort()

	return

chip_setup()
