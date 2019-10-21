from dcps import RigolDP800
from os import environ
import time, sys
from lib.Bcolors import Bcolors

class RigolDP832A():
    def __init__(self, ip):
        resource = environ.get('DP800_IP', 'TCPIP0::' + str(ip) + '::INSTR')
        self.rigol = RigolDP800(resource, 0)
        self.rigol.open()
        Bcolors.printPassed("Rigol DP832A - Connected to device on " + str(ip))
        self.rigol.beeperOff()
        self.rigol.outputOffAll()


    def set_voltage(self, voltage, channel=1):
        Bcolors.printInfo("Rigol DP832A - Setting voltage on channel " + str(channel) + " to " + str(voltage) + "V")
        self.rigol.setVoltage(voltage, channel)


    def turn_off(self, channel = 1):
        Bcolors.printInfo("Rigol DP832A - Turning OFF channel " + str(channel))
        self.rigol.outputOff(channel)

    def turn_off_all(self):
        Bcolors.printInfo("Rigol DP832A - Turning OFF all channels")
        self.rigol.outputOffAll()

    def turn_on(self, channel = 1):
        Bcolors.printInfo("Rigol DP832A - Turning ON channel " + str(channel))
        self.rigol.outputOn(channel)

    def turn_on_all(self):
        Bcolors.printInfo("Rigol DP832A - Turning ON all channels")
        self.rigol.outputOnAll()

    def stop(self):
        Bcolors.printInfo("Rigol DP832A - Stop and close connection")
        self.rigol.outputOffAll()

        # return to LOCAL mode
        self.rigol.setLocal()

        self.rigol.close()
