import mmap
import struct
import os
import re

from lib.Bcolors import Bcolors as Bc

class ProgMem:
	progmemDefined = False

	def __init__(self, programFileName):
		if ProgMem.progmemDefined:
			print(Bc.FAIL + "ERROR: progmem already opened, can only be opened once!" + Bcolors.ENDC)
			return -1
		else:
			ProgMem.progmemDefined = True

			self.programFile = open(programFileName, "r")
			self.devFile = os.open("/dev/mem",os.O_RDWR | os.O_SYNC)
			self.map = mmap.mmap(self.devFile,length=0x10000,flags=mmap.MAP_SHARED,prot=mmap.PROT_READ|mmap.PROT_WRITE,offset=0x40000000)
			self.writeProgToMem(programFileName)



	def writeProgToMem(self, programFileName):

		self.setAddress(0)
		programWords = self.programFile.readlines()

		with open(programFileName) as fp:
			line = fp.readline()
			while line:
				print("Vector instruction: {}".format(line.strip()))
				instr = re.split(' |; |, |\*|\t',line)
				addr = int(instr[0][0:4], 16)
				value = int(instr[1][0:4], 16)
				hex_string = (addr << 16) | value
				bytes = struct.unpack("4B", struct.pack(">I", hex_string))
				for byte in bytes:
					self.writeByte(byte)
				#self.map.write(bytes)
				line = fp.readline()

		# for word in programWords:
		# 	bytes = struct.unpack("4B",struct.pack("<I", int(word,16)))
		# 	for byte in bytes:
		# 		self.writeByte(chr(byte))

		self.setAddress(0)
		#byte_0 = self.readByte()
		#byte_1 = self.readByte()
		#byte_2 = self.readByte()
		#byte_3 = self.readByte()

		#print(hex(ord(byte_3)) + hex(ord(byte_2)) + hex(ord(byte_1)) + hex(ord(byte_0)))

		#self.closeProgmem()

	# get the current file pointer location
	def getAddress(self):
		return self.map.tell()

	# Set file pointer address
	def setAddress(self,adr):
		self.map.seek(adr, os.SEEK_SET)
		# Just reset program file address
		# Address indexing happens later for this file
		self.programFile.seek(0)

	# read byte from memory
	def readByte(self):
		return self.map.read_byte()

	def readWord(self):
		b1 = self.readByte()
		b2 = self.readByte()
		b3 = self.readByte()
		b4 = self.readByte()
		addr = (b1 << 8) | b2
		val = (b3 << 8) | b4
		return addr, val

	# write byte to memory
	def writeByte(self,data):
		self.map.write_byte(data)

	def checkMem(self, startAddress, stopAddress, printErrors = False):
		self.setAddress(startAddress*4)
		originalWords = self.programFile.readlines()[startAddress:stopAddress]
		#print(originalWords)
		passed = True

		for addr, word in enumerate(originalWords):
			readback = ""
			for i in range(0,4):
				readback = ("%0.2x" % ord(self.readByte())) + readback

			#print("Readback: " + readback)
			if readback != word[:-1]:
				if printErrors:
					print(Bc.WARNING + "Detected mismatch at word " + str(addr) + " : original = " + word[:-1] + " readback = " + readback + Bc.ENDC)
				passed = False

		return passed


	# Close all the files so they can be used in other objects
	def closeProgmem(self):
		self.programFile.close()
		os.close(self.devFile)

	# Change the progmem file
	def newProgmem(self, programFileName):
		self.programFile.close()
		self.programFile = open(programFileName, "r")
		self.writeProgToMem()
