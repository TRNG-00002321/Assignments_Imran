#1.Given an array arr[], find the first repeating element. The element should occur more than once and the index of its first occurrence should be the smallest.
#Examples:
#Input: arr[] = [1, 5, 3, 4, 3, 5, 6]
#Output: 2
#Explanation: 5 appears twice and its first appearance is at index 2 which is less than 3 whose first the occurring index is 3.


arr = [1,5,3,4,3,5,6]

seen = set()
for num in arr:
    if num not in seen:
        seen.add(num)
    else:
        print(arr.index(num))
        break

