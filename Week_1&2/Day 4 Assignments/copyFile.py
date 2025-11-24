#file1 = open("file01", "r")
#file2 = open("file02", "w+")

#old = file1.read()
#file2.write(old)

#ile1.close()
#file2.close()

with open("file01", "r") as file1,open("file02", "w+") as file2:
    old = file1.read()
    file2.write(old)

