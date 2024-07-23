from sys import argv

script, filename = argv
txt = open(filename)
print(f"Here's your file {filename}")
print(txt.read())
file2=open(input("Type the filename again: "))
print(file2.read())

