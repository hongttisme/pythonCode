import numpy

a = numpy.array([[1, 2], [3, 4]])

print(a[:, 1])
print()

a[0, :] = 9
print(a)
print()

a[:, 0] = 0
print(a)
print()

a[1, 1] = 7
print(a)
print()

b = numpy.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
print(b[:, 1, :])
print()

c = numpy.ones((5, 5))
print(c)
print()

c = numpy.zeros((3, 3))
print(c)
print()

d = numpy.identity(6)
print(d)
print()

e = numpy.random.randint(low=1, high=4, size=(5, 5))
a = e.copy()
print(a)
