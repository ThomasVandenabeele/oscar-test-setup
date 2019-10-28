#!/usr/bin/env python
from lib.Bcolors import Bcolors
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.commands_chip as chip
import lib.constants as const
from lib.Rigol_DP832A import RigolDP832A
from datetime import datetime
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

	print(">> Configuring power supply...")
	rigol = RigolDP832A("10.11.98.59")
	rigol.set_voltage(1, 1)
	rigol.set_voltage(1.8, 2)
	rigol.set_voltage(0, 3)
	rigol.turn_on_all()
	time.sleep(0.5)

	# Set clock frequency
	real_freq = chip.set_clock(10, writePort)
	print("Real freq: " + str(real_freq))

	time.sleep(1)

	# Send reset to the chip
	chip.reset(readPort, writePort)

	time.sleep(0.5)

	chip.enable_write_mode(writePort)
	i = 1;
	while i<101:
		chip.write_to_mem(i, i, writePort)
		# input("Press Enter to continue...")
		i = i + 1

		# input("Press Enter to continue...")
	chip.enable_exit_mode(writePort)
	# input("Press Enter to continue...")

	now = datetime.now()
	date_time = now.strftime("%m%d%Y-%H%M%S")
	filename = "../results/" + str(date_time) + "_spi-results.txt"
	chip.readout_memory(readPort, writePort, 0, 42, filename, const.RD_MEMORY)


	# Close ports
	writePort.closePort()
	readPort.closePort()
	rigol.stop()

	return

chip_setup()
