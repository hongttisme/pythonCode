x1 = int(input("Please enter the 1st number: "))
x2 = int(input("Please enter the 2nd number: "))
x3 = int(input("Please enter the 3th number: "))
x4 = int(input("Please enter the 4th number: "))
x5 = int(input("Please enter the 5th number: "))

theBiggestNUmber = x1
if theBiggestNUmber < x2:
    theBiggestNUmber = x2
if theBiggestNUmber < x3:
    theBiggestNUmber = x3
if theBiggestNUmber < x4:
    theBiggestNUmber = x4
if theBiggestNUmber < x5:
    theBiggestNUmber = x5

print(f"The biggest number among {x1},{x2},{x3},{x4},{x5} is: {theBiggestNUmber}")
