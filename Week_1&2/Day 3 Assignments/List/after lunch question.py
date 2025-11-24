#Create a list containing 5 elements (anything). Based on this list,
# create another list having elements from the previous list containing the character 'a'

a = ["fig","apple","orange","banana","peach"]

b = [fruits for fruits in a if 'a' in fruits]

print(b)

try:
    m = int(input("enter a number"))
    n = int(input("enter a number"))
    print(f"{m} / {n} = {int(m/n)}")
except ZeroDivisionError:
    print("You can't divide by zero")
except ValueError:
    print("Please enter a number")
finally:
    print("Goodbye")
