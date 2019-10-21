# from dcps import RigolDP800
# from os import environ
#
# resource = environ.get('DP800_IP', 'TCPIP0::10.11.98.59::INSTR')
# rigol = RigolDP800(resource)
# rigol.open()
# rigol.channel = 3
# rigol.setVoltage(0.4)
# rigol.outputOn()

from lib.Bcolors import Bcolors
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.commands_chip as chip
import lib.constants as const
from lib.Rigol_DP832A import RigolDP832A
from datetime import datetime
import time
import re

rigol = RigolDP832A("10.11.98.59")
rigol.turn_off_all()
rigol.set_voltage(0.5, 3)
rigol.turn_on(3)

time.sleep(2)

rigol.stop()
