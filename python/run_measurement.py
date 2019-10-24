import run_input_vector as oscar
import numpy

folderpath = "../shmoo-results/"
for freq in numpy.arange(5, 25.5, 0.5):
    result = open(folderpath + "results-" + str(freq) + ".txt", "w")

    for i in numpy.arange(1, 0.1, -0.01):
        #print(i, end=', ')
        vddc_real, freq_real, correct = oscar.run_input_vector('input_vector_C1', i, freq)
        res = "{" + str(vddc_real) + "," + str(freq_real) + "," + str(correct) + "}"
        print(res)
        result.write(res + "\n")

    # if i < 0.6:
    #     if correct == False:
    #         break

print(">> OSCAR measurement finished.")
