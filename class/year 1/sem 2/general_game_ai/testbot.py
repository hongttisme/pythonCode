import random

import numpy as np

the_map = np.ones((20, 20))
went_map = np.zeros((20, 20))
target_y = 17
target_x = 17
k = 80
while k > 0:
    y = random.randint(0, 19)
    x = random.randint(0, 19)
    the_map[y, x] = 5  # 5 == wall
    k -= 1

the_map[2, 2] = '2'  # 2 == starting place
the_map[target_y, target_x] = '3'  # 3 == ending place
went_map[2, 2] = 1
move_list = [[[0, ((17 - 2) ** 2 + (17 - 2) ** 2) ** 0.5, 2, 2]]]  # [ g(n), h(n), y, x]
print(the_map)
solution = None
searching = True
while searching:
    min_value = 100000
    the_move = None
    for moving in move_list:
        if moving[-1][0] + moving[-1][1] < min_value:
            min_value = moving[-1][0] + moving[-1][1]
            the_move = moving
    for pick in range(4):
        if pick == 1:  # up
            direction_x0 = 0
            direction_y0 = -1
        elif pick == 2:  # down
            direction_x0 = 0
            direction_y0 = 1
        elif pick == 3:  # left
            direction_x0 = -1
            direction_y0 = 0
        else:  # right
            direction_x0 = 1
            direction_y0 = 0
        the_y0 = the_move[-1][2]
        the_x0 = the_move[-1][3]
        the_y1 = the_y0 + direction_y0
        the_x1 = the_x0 + direction_x0
        if 0 <= the_y1 < 20 and 0 <= the_x1 < 20:
            if went_map[the_y1, the_x1] != 1 and the_map[the_y1, the_x1] != 5:
                new_move = the_move.copy()
                new_move.append([the_move[-1][0] + 1, ((target_y - the_y1) ** 2 + (target_x - the_x1) ** 2) ** 0.5, the_y1, the_x1])
                went_map[the_y1,the_x1] = 1
                if the_map[the_y1,the_x1] == 3:
                    solution = new_move
                    searching = False
                    break
                else:
                    move_list.append(new_move)
    move_list.remove(the_move)
print(solution)
for moving in solution:
    the_map[moving[2],moving[3]] = 0

print(the_map)