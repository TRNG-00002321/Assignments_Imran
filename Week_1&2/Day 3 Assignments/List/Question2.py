#2. You are given a number k and a list arr[] that contains integers.
# You need to return list of numbers that are less than k.

k = 2
arr = [-2,345,5,6,6,7,43,-52,-2,41,41,1]

ret = [num for num in arr if num < k]

print(ret)

