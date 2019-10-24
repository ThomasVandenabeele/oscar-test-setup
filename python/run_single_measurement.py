import run_input_vector as oscar
import numpy

result = open("results-5.txt", "a")
freq = 5
vddc = 0.44

#for i in numpy.arange(0.4, 0.1, -0.02):
#print(i, end=', ')
vddc_real, freq_real, correct = oscar.run_input_vector('input_vector_C1', vddc, freq)
res = "{" + str(vddc_real) + "," + str(freq_real) + "," + str(correct) + "}"
print(res)
result.write(res + "\n")
# if i < 0.6:
#     if correct == False:
#         break
