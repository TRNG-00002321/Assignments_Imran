#2. Given a string s, you need to check if it is palindrome or not.
# A palidrome is a string that reads the same from front and back.


s = "lolol"

if s == s[::-1]:
    print(f"The word {s} is the same flipped")
else:
    print(f"The word {s} is not the same when flipped")
