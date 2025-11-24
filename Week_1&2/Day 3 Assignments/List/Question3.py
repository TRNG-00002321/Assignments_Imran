import numpy as np

arr = np.array([-12, 8, -7, 6, 12, -9, 14])
positive = arr[arr >= 0]
average = np.mean(positive)
print("Average of non-negative integers:", average)