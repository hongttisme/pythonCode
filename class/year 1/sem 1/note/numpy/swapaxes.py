import numpy as np
a = np.arange(1,11)
print(a)

a = a.reshape((2,5))
print(a)

a = a.swapaxes(0,1)
print(a)
