n = 0
while (n % 2) == 0 or n < 0:
    n = int(input("input a positive odd number: "))

r = n

while n >= 1:
    for x in range(1,r-n + 1):
        print(" ",end='')
    for x in range(1, n + 1, 1):
        print('*', end=' ')
    print('')
    n -= 2
