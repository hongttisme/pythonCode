import numpy
def mini_edit_dis(s1, s2):
  print(f"how to make {s1} become a {s2}")
  in_size = len(s1) + 1
  out_size = len(s2) + 1
  count_table = numpy.zeros((in_size, out_size))
  #
  pace_table = numpy.zeros((in_size, out_size))

  # 1 is del, 2 is add, 3 is sub, 4 is skip
  for x in range(in_size):
    count_table[x,0] = x
    pace_table[x, 0] = 1

  for x in range(1,out_size):
    count_table[0,x] = x
    pace_table[0, x] = 2


  for x in range(1,in_size):
    for y in range(1,out_size):
      the_num = count_table[x-1,y-1]
      k = 4
      if s1[x-1] != s2[y-1]:
        the_num += 2
        k = 3
      if count_table[x - 1,y] + 1< the_num:
        the_num = count_table[x-1,y] + 1
        k = 1
      if count_table[x,y-1] + 1< the_num:
        the_num = count_table[x, y-1] + 1
        k = 2
      count_table[x,y] = the_num
      pace_table[ x,y] = k

  x0 = in_size - 1
  y0 = out_size - 1
  string_list = []
  while not (x0 == y0 and x0 == 0):
    if pace_table[x0,y0] == 4:
      x0 -= 1
      y0 -= 1

    elif pace_table[x0,y0] == 3:
      string_list.append(f'sub {s1[x0-1]} to {s2[y0-1]}: {s2[:y0-1]+s1[x0-1:]} -> {s2[:y0]+s1[x0:]}')

      x0 -= 1
      y0 -= 1
    elif pace_table[x0, y0] == 2:
      string_list.append(f'add {s2[y0-1]}: {s2[:y0-1]+s1[x0-1:]} -> {s2[:y0]+s1[x0-1:]}')
      y0 -= 1
    elif pace_table[x0, y0] == 1:
      string_list.append(f'del {s1[x0-1]}: {s2[:y0]+s1[x0-1:]} -> {s2[:y0]+s1[x0:]}')

      x0-= 1

  for x in range(len(string_list)):
    print("step", x + 1,":",string_list[-(x + 1)])
  return count_table


print(int(mini_edit_dis("zheng dong", "dog")[-1,-1]), "step is required")
# 右边到左边 = add （2） 下到上 = del （1）


