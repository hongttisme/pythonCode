import numpy as np

f = np.loadtxt("test", skiprows=1, delimiter=',', dtype=np.int32)
print(f)
print(f.dtype)
np.savetxt("testout", f, delimiter=';', fmt="%d", header="a;b;c;d", comments='')

f = np.genfromtxt("test1", skip_header=1, filling_values=0, delimiter=',', dtype=np.int32)
print(f)  # almost same with loadtxt but fill up the missing values
