#!/usr/bin/env python
from lib.Bcolors import Bcolors
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.commands_chip as chip
import lib.constants as const
import lib.compare_results as compare_results
from lib.Rigol_DP832A import RigolDP832A
from datetime import datetime
import time
import re
import yaml
import difflib

print(">> Checking results...")
vectorfn = 'input_vector_C1'
filename = "../results/test.txt"
configfn = "../input_vectors/" + vectorfn + ".config"
outputfn = "../output_vectors/" + vectorfn + ".out"
vectorreffn = "../input_vectors/" + vectorfn + ".out"

compare_results.check(configfn, vectorreffn, filename, outputfn)
