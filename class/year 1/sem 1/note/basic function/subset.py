s1 = {2, 4, 6}
s2 = {1, 2, 3, 4, 5, 6}
if s1.issubset(s2):
    print("s1 is subset of s2")
if s2.issubset(s1):
    print("s2 is superset of s1")


s1.update([8])

print(s1)
s1.remove(2)
print(s1)
s1.update([8])
print(s1)
a = dict()
a[234] = 3
print(a)



