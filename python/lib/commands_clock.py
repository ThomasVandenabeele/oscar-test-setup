#!/usr/bin/env python
import os
import numpy as np
from lib.Bcolors import Bcolors
import lib.FPGA_ISA as instructions
from lib.WritePort import WritePort
import lib.constants as cnst

class Clock:
	clockDefined = False

	drpAddressMap = {"Power Reg"     : 0x28,
					 "CLKOUT0 Reg1"  : 0x08,
					 "CLKOUT0 Reg2"  : 0x09,
					 "CLKOUT1 Reg1"  : 0x0A,
					 "CLKOUT1 Reg2"  : 0x0B,
					 "CLKOUT2 Reg1"  : 0x0C,
					 "CLKOUT2 Reg2"  : 0x0D,
					 "CLKOUT3 Reg1"  : 0x0E,
					 "CLKOUT3 Reg2"  : 0x0F,
					 "CLKOUT4 Reg1"  : 0x10,
					 "CLKOUT4 Reg2"  : 0x11,
					 "CLKOUT5 Reg1"  : 0x06,
					 "CLKOUT5 Reg2"  : 0x07,
					 "CLKOUT6 Reg1"  : 0x12,
					 "CLKOUT6 Reg2"  : 0x13,
					 "DIV_CLK Reg"   : 0x16,
					 "CLKFBOUT Reg1" : 0x14,
					 "CLKFBOUT Reg2" : 0x15,
					 "LOCK Reg1"     : 0x18,
					 "LOCK Reg2"     : 0x19,
					 "LOCK Reg3"     : 0x1A,
					 "Filter Reg1"   : 0x4E,
					 "Filter Reg2 "  : 0x4F}

	def __init__(self):
		if Clock.clockDefined:
			Bcolors.printError("clock already constructed, only one clock object can exist!")
			return -1
		else:
			Clock.clockDefined = True

#			self.devFile = os.open("/dev/mem",os.O_RDWR | os.O_SYNC)
#			self.map = mmap.mmap(self.devFile,length=0x1FFF,flags=mmap.MAP_SHARED,prot=mmap.PROT_READ|mmap.PROT_WRITE,offset=0x40009000)
			self.inputFrequency = 100e6
			frequencies = []
			for freqFile in os.listdir(cnst.PROJDIR + "/python/lookup_data/"):
				if freqFile.endswith(".csv"):
					frequencies.append((freqFile[5:-4]))
			self.frequencies = np.asarray(frequencies,dtype=float)

	def getFrequencies(self):
		return self.frequencies

	def findNearestFrequency(self, frequency, verbose=False):
		idx = (abs(self.frequencies-frequency)).argmin()
		if verbose:
			Bcolors.printInfo("Nearest frequency = " + str(self.frequencies[idx]) + " for requested frequency " + str(frequency))
		return self.frequencies[idx]

	def setFrequency(self,frequency,writePort,verbose=True):
		## Set extra 8 divisor on or off +
		#if frequency < 5:
		#	extraDivOn = True
		#else:
		#	extraDivOn = False
		#
		##reset mmcm for configuration + set divider on/off
		#self.map.seek(0x0000,os.SEEK_SET)
		#if extraDivOn:
		#	self.map.write_byte(chr(0x03))
		#else:
		#	self.map.write_byte(chr(0x01))
		#
		## Set power register
		#self.map.seek(0x10A0,os.SEEK_SET)
		#self.map.write(struct.pack("I",0x0000FFFF))

		# Find nearest frequency, this frequency will be used
		#if extraDivOn:
		#	exactFrequency = self.findNearestFrequency(frequency*8,verbose)
		#else:
		#	exactFrequency = self.findNearestFrequency(frequency,verbose)
		instruction = (instructions.chip_setclk << 29) | (0x28 << 16) | (0xFFFF)
		writePort.sendInt(instruction)

		exactFrequency = self.findNearestFrequency(frequency,verbose)

		with open(cnst.PROJDIR + "/python/lookup_data/freq_" + "%.2f" % exactFrequency + ".csv","r") as lookUpFile:
			for i, line in enumerate(lookUpFile):
				if i != 0:
					regName, fakeAddr, value = line.split(",")
					if verbose:
						Bcolors.printInfo(regName + "address:" + str(Clock.drpAddressMap[regName[1:-1]]) + " value: " + hex(int(value,16)))
					addr = Clock.drpAddressMap[regName[1:-1]]
					instruction = (instructions.chip_setclk << 29) | (addr << 16) | int(value,16)
					writePort.sendInt(instruction)
					#self.map.seek(0x1000 + 4*Clock.drpAddressMap[regName[1:-1]],os.SEEK_SET)
					#self.map.write(struct.pack("I",int(value,16)))
					#time.sleep(0.001)

		#if verbose:
		#	self.printDRPRegisters()

		#self.map.seek(0x0000,os.SEEK_SET)
		#if extraDivOn:
		#	self.map.write_byte(chr(0x02))
		#	return exactFrequency/8
		#else:
		#	self.map.write_byte(chr(0x00))
		#	return exactFrequency
		return exactFrequency

	# Close all the files so they can be used in other objects
	def closeClock(self):
		os.close(self.devFile)
