seconds = int(input("Please enter number of seconds : "))
minutes = seconds // 60
seconds = seconds % 60
hours = minutes // 60
minutes = minutes % 60
days = hours // 24
hours = hours % 24
print(f"The output is: {days}days, {hours}hours, {minutes}minutes, {seconds}seconds")
