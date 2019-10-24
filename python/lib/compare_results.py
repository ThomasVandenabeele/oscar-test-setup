#!/usr/bin/env python
from lib.Bcolors import Bcolors
import yaml
import difflib

def check(configfn, reffn, oscarfn, outputfn):
    #vectorfn = 'input_vector_C1'
    filename = oscarfn #"../results/test.txt"

    #configfn = "../input_vectors/" + vectorfn + ".config"

    with open(configfn, 'r') as cfgfile:
        cfg = yaml.load(cfgfile, yaml.Loader)
    ct_size = cfg['plaintext_size']
    tag_size = cfg['tag_size']

    #outputfn = "../output_vectors/" + vectorfn + ".out"
    out = open(outputfn, "w")
    out.write("#C\n")
    with open(filename) as fp:
       line = fp.readline()
       while line:
           byte1 = line[0:2]
           byte2 = line[2:4]

           for i in range(2):
               if ct_size > 0:
                   out.write(line[i*2 : i*2+2].upper() + "\n")
                   ct_size -= 1
               elif ct_size == 0:
                   if tag_size == cfg['tag_size']:
                       out.write("#T\n")
                       line = fp.readline()
           if ct_size == 0:
               for i in range(2):
                   if tag_size > 0:
                       out.write(line[i*2 : i*2+2].upper() + "\n")
                       tag_size -= 1

           line = fp.readline()
    out.close()

    with open(outputfn) as f1:
    		f1_text = f1.read()

    # vectorreffn = "../input_vectors/" + vectorfn + ".out"
    vectorreffn = reffn
    with open(vectorreffn) as f2:
    	f2_text = f2.read()

    diffs = []
    for line in difflib.unified_diff(f2_text, f1_text, fromfile='Ketje reference', tofile='OSCAR out', lineterm=''):
    	#print(line)
    	diffs.append(line)

    correct = True
    if not diffs:
        Bcolors.printPassed("SUCCES - Correct output")
    	# print("\t\t\t\t\t\t\033[92m" + "SUCCES: Correct output" + "\033[0m")
    else:
        correct = False
        Bcolors.printError("Corrupted output")
    	#print("\t\t\t\t\t\t\033[91m" + "ERROR: Corrupted output" + "\033[0m")
    return correct
