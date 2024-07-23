n = 0
while (n % 2) == 0 or n < 0:
    n = int(input("input a positive odd number: "))
x = 1
the_sum = 0
while x <= n:
    the_sum += x
    x += 2
print(the_sum)
