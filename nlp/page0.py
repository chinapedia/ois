# pip3 install numpy

import numpy
inputArray = [
    [ 0, 1, 2, 3, 4], 
    [ 5, 6, 7, 8, 9], 
    [10, 11, 12, 13, 14]] 
npa = numpy.array(inputArray)
results = [numpy.average(npa, axis = 0), numpy.average(npa, axis = 1)]
print ([x.tolist() for x in results])
