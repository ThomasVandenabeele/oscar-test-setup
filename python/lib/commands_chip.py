#!/usr/bin/env python
from lib.Bcolors import Bcolors
import lib.FPGA_ISA as instructions
from lib.WritePort import WritePort
from lib.commands_clock import Clock
import time

def reset(readPort, writePort):
	Bcolors.printInfo("Resetting ... ")
	toggle_reset(writePort)
	time.sleep(0.1)
	toggle_reset(writePort)

	#before starting measurement, clearing the values from the FIFO
	clear_results(readPort)


def toggle_reset(writePort):
    instruction = (instructions.chip_reset << 29)
    writePort.sendInt(instruction)

def start(writePort):
	Bcolors.printInfo("Sending start pulse ...")
	instruction = (instructions.chip_start << 29)
	writePort.sendInt(instruction)

def enable_write_mode(writePort):
	Bcolors.printInfo("Enabling write mode ...")
	data = (4095 << 4) | 1 #FFF1
	#Bcolors.printInfo("Instruction: " + "0x{:04x}".format(data))
	instruction = (instructions.spi_write << 29) | data
	writePort.sendInt(instruction)

def enable_read_mode(memory, writePort):
	Bcolors.printInfo("Enabling READ mode for memory " + str(memory) + " ...")
	data = (4095 << 4) | (memory << 2) | 0
	#Bcolors.printInfo("Instruction: " + "0x{:04x}".format(data))
	instruction = (instructions.spi_write << 29) | data
	writePort.sendInt(instruction)

def enable_exit_mode(writePort):
	Bcolors.printInfo("Enabling EXIT mode ...")
	data = (4095 << 4) | 3
	#Bcolors.printInfo("Instruction: " + "0x{:04x}".format(data))
	instruction  = (instructions.spi_write << 29) | data
	writePort.sendInt(instruction)

def write_mem(n_addr, writePort):
	Bcolors.printInfo("Writing memory from 0 to {} ...".format(n_addr))
	instruction  = (instructions.write_prog << 29) | n_addr
	#Bcolors.printInfo("Instruction: " + "0x{:04x}".format(instruction))
	writePort.sendInt(instruction)

def write_to_mem(addr, data, writePort):
	Bcolors.printInfo("Write " + str(data) + " to addr " + str(addr))
	instruction_addr = (instructions.spi_write << 29) | addr
	#Bcolors.printInfo("Instruction: " + "0x{:04x}".format(addr))
	writePort.sendInt(instruction_addr)
	instruction_data = (instructions.spi_write << 29) | data
	#Bcolors.printInfo("Instruction: " + "0x{:04x}".format(data))
	writePort.sendInt(instruction_data)

def read_addr(addr, writePort):
	instruction  = (instructions.spi_write << 29) | addr
	Bcolors.printInfo("Reading addr " + str(addr))
	#Bcolors.printInfo("Instruction: " + "0x{:04x}".format(addr))
	writePort.sendInt(instruction)

def clear_results(readPort):
	i=0
	while i<2048:
		readPort.readInt()
		i = i + 1

def readout_results(readPort, filename, n_results=2048):
	if not filename is None:
		file=open(filename,'a')

	# Read the values
	i=0
	while i<n_results:
		data = readPort.readInt()
		if not data is None:
			print("Readback: " + "0x{:04x}".format(data))
			if not filename is None:
				file.write("{:04x}".format(data) + "\n")
		i=i+1
	if not filename is None:
		file.close()

def readout_memory(readPort, writePort, start, end, filename, memory=0):
	enable_read_mode(memory, writePort)
	#input("Press Enter to continue...")

	i = start;
	while i<=end:
		read_addr(i, writePort)
		if i == start:
			clear_results(readPort)
			#input("Press Enter to continue...")
		i = i + 1

	#input("Press Enter to continue...")
	enable_exit_mode(writePort)

	time.sleep(0.5)
	readout_results(readPort, filename, end-start+1)

def set_clock(frequency, writePort):
	clock = Clock()
	freq  = clock.setFrequency(frequency, writePort)
	
	return freq
