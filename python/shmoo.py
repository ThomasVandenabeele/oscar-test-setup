import re
from os import listdir
from os.path import isfile, join

# def find_shmoo_coordinate(fn):
#     result_freq = fn #'results-5.txt'
#     coordinate = 0, 0
#
#     with open(result_freq) as fp:
#         falsecount = 0
#         line = fp.readline()[1:-1]
#
#         while line:
#             values = re.split(',', line)
#
#             vdd = float(values[0])
#             freq = float(values[1])
#             correct = values[2]
#
#             if "False" in correct:
#                 falsecount += 1
#                 if falsecount == 25:
#                     break
#             else:
#                 falsecount = 0
#                 coordinate = freq, vdd
#
#             line = fp.readline()[1:-1]
#
#     print(str(coordinate))
#     return coordinate

def find_shmoo_coordinate(fn):
    result_freq = fn #'results-5.txt'
    unc_coordinate = 0, 0
    fail_coordinate = 0, 0

    with open(result_freq) as fp:
        line = fp.readline()[1:-1]

        while line:
            [co, vals] = re.split('\[\[', line)
            vdd, freq, no = re.split(',', co)
            if vals.count("True") < 100:
                if str(unc_coordinate) == "(0, 0)":
                    unc_coordinate = float(freq), float(vdd)

                if vals.count("False") == 100:
                    fail_coordinate = float(freq), float(vdd)
                    break
            # vdd = float(values[0])
            # freq = float(values[1])
            # correct = values[2]

            # if "False" in correct:
            #     falsecount += 1
            #     if falsecount == 25:
            #         break
            # else:
            #     falsecount = 0
            #     coordinate = freq, vdd

            line = fp.readline()[1:-1]

    # print(str(coordinate))
    return unc_coordinate, fail_coordinate

def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]

mypath = "../shmoo-test"
filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
outputfn = "shmoo.tex";
filenames.sort(key=natural_keys)
# print(filenames)

unc_fn = "unc_" + outputfn
fail_fn = "fail_" + outputfn

unc_out = open(unc_fn, "w")
fail_out = open(fail_fn, "w")
for file in filenames:
    unc_co, fail_co = find_shmoo_coordinate(mypath + "/" + file)
    # print(str(unc_co))
    unc_out.write(str(unc_co) + "\n")
    fail_out.write(str(fail_co) + "\n")
unc_out.close()
fail_out.close()

with open(unc_fn, 'r') as reader:
    print(reader.read())

print("------------------\n")

with open(fail_fn, 'r') as reader:
    print(reader.read())
