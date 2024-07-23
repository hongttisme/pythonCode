import random
import time
import numpy as np
n = 10000 # here to change the n
unsort_list = np.array(list(range(n)))
np.random.shuffle(unsort_list)

copy_of_list = np.copy(unsort_list)
t1 = time.time()

for i in range(n):
    the_min_id = i
    the_min = copy_of_list[the_min_id]
    for j in range(i + 1, n):
        if copy_of_list[j] < the_min:
            the_min_id = j
            the_min = copy_of_list[the_min_id]

    copy_of_list[the_min_id] = copy_of_list[i]
    copy_of_list[i] = the_min

t2 = time.time()
print(t2 - t1)
copy_of_list