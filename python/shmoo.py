import re
from os import listdir
from os.path import isfile, join

def find_shmoo_coordinate(fn):
    result_freq = fn #'results-5.txt'
    coordinate = 0, 0

    with open(result_freq) as fp:
        falsecount = 0
        line = fp.readline()[1:-1]

        while line:
            values = re.split(',', line)

            vdd = float(values[0])
            freq = float(values[1])
            correct = values[2]

            if "False" in correct:
                falsecount += 1
                if falsecount == 25:
                    break
            else:
                falsecount = 0
                coordinate = freq, vdd

            line = fp.readline()[1:-1]

    print(str(coordinate))
    return coordinate

def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]

mypath = "../shmoo-results"
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
outputfn = "shmoo.tex";
filenames.sort(key=natural_keys)
print(filenames)


out = open(outputfn, "w")
for file in filenames:
    coor = find_shmoo_coordinate(mypath + "/" + file)
    out.write(str(coor) + "\n")
