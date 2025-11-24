from functools import reduce

# 1. Filter Strings by Length
words = ["apple", "banana", "cat", "dog", "elephant", "frog"]
long_words = list(filter(lambda w: len(w) > 5, words))
print(long_words)

# 2. Filter Students by Grade
students = [
    {"name": "Alice", "grade": 85},
    {"name": "Bob", "grade": 92},
    {"name": "Charlie", "grade": 78},
    {"name": "David", "grade": 95}
]
top_students = list(filter(lambda s: s["grade"] >= 90, students))
print(top_students)

# 3. Concatenate Strings
words = ["Python", "is", "awesome", "!"]
sentence = reduce(lambda a, b: a + " " + b, words)
print(sentence)

# 4. Find the Maximum Element
numbers = [10, 3, 25, 7, 18]
max_number = reduce(lambda a, b: a if a > b else b, numbers)
print(max_number)

# 5. Flatten a List of Lists
list_of_lists = [[1, 2], [3, 4], [5, 6]]
flattened = reduce(lambda a, b: a + b, list_of_lists)
print(flattened)
