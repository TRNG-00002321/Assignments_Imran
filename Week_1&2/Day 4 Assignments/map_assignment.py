# 1. Convert Celsius to Fahrenheit
celsius_temps = [0, 10, 20, 30]
fahrenheit_temps = list(map(lambda c: (c * 9/5) + 32, celsius_temps))
print(fahrenheit_temps)

# 2. Capitalize a List of Names
names = ["alice", "bob", "charlie"]
capitalized_names = list(map(lambda n: n.capitalize(), names))
print(capitalized_names)

# 3. Add Corresponding Elements
list1 = [1, 2, 3]
list2 = [4, 5, 6]
sums = list(map(lambda a, b: a + b, list1, list2))
print(sums)

# 4. Concatenate Strings
first_names = ["John", "Jane"]
last_names = ["Doe", "Smith"]
full_names = list(map(lambda a, b: a + " " + b, first_names, last_names))
print(full_names)

# 5. Apply a Custom Function
def get_length(s):
    return len(s)

words = ["apple", "banana", "cherry"]
lengths = list(map(get_length, words))
print(lengths)
