#2. Given three inputs that are stored in the variables a, b, and c.
# You need to print a a times and b b times  in a single line separated by c.


a = input("Enter a number:")
b = input("Enter another number:")
c = input("Enter a special character:")

print(a * int(a) + c + b * int(b))