with open('WriteThisFIle', 'w') as f:
    # f.truncate()
    f.write("hihi")
    f.write("bye")
# writelines is for write some list into a file
with open('WriteThisFIle', 'r') as f:
    # f.truncate()
    text = f.read()

print(text)
