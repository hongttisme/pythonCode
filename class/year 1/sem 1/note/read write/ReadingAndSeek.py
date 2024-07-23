f = open('theTxt', encoding="utf-8")
f.seek(4)  # Go to the 4th byte in the file
# print(f.read()) # read all
# print(f.read(1))  # e
# print(f.read(3))  # fgh (continue reading)
f.close()
