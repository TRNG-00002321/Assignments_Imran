# 1. Country and Capital Dictionary
countries = {
    "India": "New Delhi",
    "USA": "Washington D.C.",
    "France": "Paris",
    "Japan": "Tokyo",
    "Canada": "Ottawa"
}

def get_capital(country):
    return countries.get(country, "Country not found")

print(get_capital("Japan"))

# 2. Student Scores Dictionary
students = {
    "Alice": 85,
    "Bob": 92,
    "Charlie": 78,
    "David": 95,
    "Eve": 88
}

def top_student(scores):
    return max(scores, key=scores.get)

print("Top student:", top_student(students))

# 3. Nested Employee Dictionary with 10% Raise
employees = {
    "emp1": {"name": "John", "age": 25, "salary": 50000},
    "emp2": {"name": "Mary", "age": 30, "salary": 60000},
    "emp3": {"name": "Ali", "age": 28, "salary": 55000}
}

def give_raise(emp_dict):
    for emp in emp_dict.values():
        emp["salary"] = emp["salary"] * 1.10
    return emp_dict

print(give_raise(employees))

# 4. Add a Key to Dictionary
dictionary = {"Name": "Ram", "Age": 23}
add_key = {"City": "Salem"}
dictionary.update(add_key)
print(dictionary)

# 5. Concatenate Dictionaries
dict1 = {"Name": "Ram", "Age": 23}
dict2 = {"City": "Salem", "Gender": "Male"}
concatenated = {**dict1, **dict2}
print(concatenated)

# 6. Check if Key Exists
data = {"Name": "Ram", "Age": 23}
key = "Name"
if key in data:
    print("Key is Available in the Dictionary")
else:
    print("Key is not Available in the Dictionary")

# 7. Iterate Over Dictionary
person = {"Name": "Ram", "Age": 23, "City": "Salem", "Gender": "Male"}
for k, v in person.items():
    print(k, ":", v)
