a = [[[73, 127], [1, 35]], [[73, 126], [1, 41]], [[73, 138], [1, 44]], [[73, 132], [1, 38]], [[73, 134], [1, 44]], [[73, 129], [1, 51]], [[73, 137], [1, 53]], [[73, 140], [1, 49]], [[73, 112], [1, 27]], [[73, 129], [1, 36]]]
land_ave = 0
land_var = 0
army_ave = 0
army_var = 0

for k in a:
    land_ave += k[1][1]
    army_ave += k[0][1]
land_ave = land_ave/10
army_ave = army_ave/10
for k in a:
    land_var += (k[1][1] - land_ave) ** 2
    army_var += (k[1][1] - army_ave) ** 2
land_var = land_var/9
army_var = army_var/9

print(f"{land_ave=}, {land_var=}, {army_ave=}, {army_var=}")
