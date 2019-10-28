import run_input_vector as oscar
import numpy

#folderpath = "../shmoo-results/"
#for freq in numpy.arange(5, 25.5, 0.5):
#    result = open(folderpath + "results-" + str(freq) + ".txt", "w")

#    for i in numpy.arange(0.8, 0.1, -0.01):
        #print(i, end=', ')
big_result_array = []
#        for ntimesbig in range(10):
vddc_real, freq_real, result_array = oscar.run_input_vector('input_vector_C1', 0.7, 20)
big_result_array.append(result_array)
res = "{" + str(vddc_real) + "," + str(freq_real) + "," + str(big_result_array) + "}"
print(res)
# result.write(res + "\n")

    # if i < 0.6:
    #     if correct == False:
    #         break

print(">> OSCAR measurement finished.")
