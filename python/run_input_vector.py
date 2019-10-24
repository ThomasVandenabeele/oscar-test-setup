#!/usr/bin/env python
from lib.Bcolors import Bcolors
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.commands_chip as chip
import lib.constants as const
from lib.Rigol_DP832A import RigolDP832A
import lib.compare_results as compare_results
from datetime import datetime
import time
import re
import yaml

def run_input_vector(name, vddc, clockfreq):
    vectorfn = name
    # vectorfn = 'input_vector_C1'
    configfn = "../input_vectors/" + vectorfn + ".config"

    # print("OSCAR MEASUREMENT SETUP")
    # print("Thomas Vandenabeele\n")
    #Setup read and write port
    writePort = WritePort("/dev/xillybus_write_32",32)
    readPort  = ReadPort("/dev/xillybus_read_32",32)

    print(">> Connecting to FIFOs...")
    if not writePort.openPort():
        print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)
        quit()
    if not readPort.openPort():
        print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)

    # Reading settings
    with open(configfn, 'r') as cfgfile:
        cfg = yaml.load(cfgfile, yaml.Loader)

    print(">> Configuring power supply...")
    rigol = RigolDP832A("10.11.98.59")
    rigol.set_voltage(cfg['vdd'], 1)
    rigol.set_voltage(cfg['vdde'], 2)
    rigol.set_voltage(vddc, 3)
    rigol.turn_on_all()
    time.sleep(0.5)

    print(">> Configuring clock frequency...")
    # Set clock frequency
    real_freq = chip.set_clock(clockfreq, writePort)
    #print("Real freq: " + str(real_freq))
    Bcolors.printPassed("CLOCK - Real frequency is " + str(real_freq) + "MHz")

    time.sleep(1)

    print(">> Sending reset pulse...")
    # Reset chip
    chip.reset(readPort, writePort)


    time.sleep(0.5)

    # Send a program to the chip
    print(">> Sending data to memory...")
    chip.enable_write_mode(writePort)
    vector = '../input_vectors/' + vectorfn + '.in'
    with open(vector) as fp:
       line = fp.readline()
       while line:
           #print("Vector instruction: {}".format(line.strip()))
           instr = re.split(' |; |, |\*|\t',line)

           addr = (int(instr[0][0:4], 16))
           value = (int(instr[1][0:4], 16))
           chip.write_to_mem(addr, value, writePort)
           line = fp.readline()

    #input("Press Enter to continue...")
    chip.enable_exit_mode(writePort)
    #input("Change clock and press Enter to continue...")

    time.sleep(0.5)

    print(">> Sending start pulse...")
    chip.start(writePort)

    time.sleep(5)

    print(">> Reading back results...")
    now = datetime.now()
    date_time = now.strftime("%m%d-%H%M%S")
    filename = "../results/" + str(date_time) + "_spi-results.txt"
    chip.readout_memory(readPort, writePort, 0, 7, filename, const.WR_MEMORY)

    print(">> Checking results...")
    outputfn = "../output_vectors/" + vectorfn + ".out"
    vectorreffn = "../input_vectors/" + vectorfn + ".out"

    correct = compare_results.check(configfn, vectorreffn, filename, outputfn)

    # with open("../input_vectors/" + vectorfn + ".config", 'r') as cfgfile:
    #     cfg = yaml.load(cfgfile, yaml.Loader)
    # ct_size = cfg['plaintext_size']
    # tag_size = cfg['tag_size']
    #
    # out = open("../output_vectors/" + vectorfn + ".out", "w")
    # out.write("#C\n")
    # with open(filename) as fp:
    #    line = fp.readline()
    #    while line:
    #        byte1 = line[0:2]
    #        byte2 = line[2:4]
    #
    #        for i in range(2):
    #            if ct_size > 0:
    #                out.write(line[i*2 : i*2+2].upper() + "\n")
    #                ct_size -= 1
    #            elif ct_size == 0:
    #                if tag_size == cfg['tag_size']:
    #                    out.write("#T\n")
    #                    line = fp.readline()
    #        if ct_size == 0:
    #            for i in range(2):
    #                if tag_size > 0:
    #                    out.write(line[i*2 : i*2+2].upper() + "\n")
    #                    tag_size -= 1
    #
    #        line = fp.readline()
    # out.close()


    vddc_real = rigol.get_real_voltage(3)

    print(">> Closing connections...")
    # Close ports
    writePort.closePort()
    readPort.closePort()
    
    rigol.stop()

    return vddc_real, real_freq, correct
