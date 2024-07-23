def sum_num(x, y):
    result = 0
    for i in range(x, y + 1):
        result += i
    return result


print(f"sum from 1 to 10 is {sum_num(1, 10)}")
