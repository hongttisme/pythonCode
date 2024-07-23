with open("aboutMe", 'r') as file:
    f = file.read()
    print(f)

with open("aboutMe", 'a') as file:
    file.write('\n')
    file.write("AIT2304041")
