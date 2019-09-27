#!/usr/bin/env python
from lib.Bcolors import Bcolors
import lib.FPGA_ISA as instructions
from lib.WritePort import WritePort
import time

def reset(writePort):
	Bcolors.printInfo("Resetting ... ")
	toggle_reset(writePort)
	time.sleep(0.1)
	toggle_reset(writePort)

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
	Bcolors.printInfo("Instruction: " + "0x{:04x}".format(data))
	instruction = (instructions.spi_write << 29) | data
	writePort.sendInt(instruction)

def enable_read_mode(memory, writePort):
	Bcolors.printInfo("Enabling READ mode for memory " + str(memory) + " ...")
	data = (4095 << 4) | (memory << 2) | 0
	Bcolors.printInfo("Instruction: " + "0x{:04x}".format(data))
	instruction = (instructions.spi_write << 29) | data
	writePort.sendInt(instruction)

def enable_exit_mode(writePort):
	Bcolors.printInfo("Enabling EXIT mode ...")
	data = (4095 << 4) | 3
	Bcolors.printInfo("Instruction: " + "0x{:04x}".format(data))
	instruction  = (instructions.spi_write << 29) | data
	writePort.sendInt(instruction)

def write_to_mem(addr, data, writePort):
	Bcolors.printInfo("Write " + str(data) + " to addr " + str(addr))
	instruction_addr = (instructions.spi_write << 29) | addr
	Bcolors.printInfo("Instruction: " + "0x{:04x}".format(addr))
	writePort.sendInt(instruction_addr)
	instruction_data = (instructions.spi_write << 29) | data
	Bcolors.printInfo("Instruction: " + "0x{:04x}".format(data))
	writePort.sendInt(instruction_data)

def read_addr(addr, writePort):
	Bcolors.printInfo("Reading addr " + str(addr))
	Bcolors.printInfo("Instruction: " + "0x{:04x}".format(addr))
	writePort.sendInt(addr)
