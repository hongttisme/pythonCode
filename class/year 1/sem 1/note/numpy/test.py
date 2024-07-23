import numpy
the_one = numpy.ones(shape=(5,5))
print(the_one)
the_one = numpy.pad(the_one,((1,1),(1,1)),constant_values=0)
print(the_one)
a = numpy.array([[1,2,3],[4,5,6]])
a = a.T
print(a)