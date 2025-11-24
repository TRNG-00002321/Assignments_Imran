#1. You are given an array arr[] of size n. You have to insert all elements of arr[] into a set and return that set .
#You are also given a interger x. If x is found in set then erase it from set and print "erased x", otherwise, print "not found".

arr = [1,2,3,4,5,6,7]
n = int(input("number plz: "))

arr  = set(arr)

if n in arr:
    arr.remove(n)
    print("erased", n)
else:
    print("not found")
