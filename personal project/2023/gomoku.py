import numpy as np

the_map = np.zeros(shape=(15, 15))
print(the_map)


def check_local(x, y):
    if the_map[x - 2, y] == the_map[x - 1, y] == the_map[x, y] == the_map[x + 1, y] == the_map[x + 2, y] and the_map[x, y] != 0:
        return True
    elif the_map[x - 2, y - 2] == the_map[x - 1, y - 1] == the_map[x, y] == the_map[x + 1, y + 1] == the_map[x + 2, y + 2] and the_map[x, y] != 0:
        return True
    elif the_map[x - 2, y + 2] == the_map[x - 1, y + 1] == the_map[x, y] == the_map[x + 1, y - 1] == the_map[x + 2, y - 2] and the_map[x, y] != 0:
        return True
    elif the_map[x, y - 2] == the_map[x, y - 1] == the_map[x, y] == the_map[x, y + 1] == the_map[x, y + 2] and the_map[x, y] != 0:
        return True
    else:
        return False


def check_map():
    for r in range(11):
        for c in range(11):
            local_return = check_local(r, c)
            if local_return:
                return local_return

    return False


game_continue = True
player = -1
while game_continue:
    player *= -1
    x = int(input())
    y = int(input())
    if the_map[x, y] != 0:
        print("wrong input!")
        player *= -1
        continue
    else:
        the_map[x, y] = player

    print(the_map)

    game_continue = not check_map()
    if not game_continue:
        print("game end!")
