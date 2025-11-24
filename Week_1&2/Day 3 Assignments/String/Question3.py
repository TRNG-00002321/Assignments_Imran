#3. Given a string s, and a pattern p. You need to find if p exists in s or not and return the starting index of p in s.
# If p does not exist in s then -1 will be returned.
#Here p and s both are case-sensitive.
#Examples:
#Input: s = "Hello", p = "llo"
#Output: 2
#Explanation: llo starts from the second index in Hello.

s = input("Enter a string: ")
p = input("Enter a pattern: ")

if p in s:
    position = s.find(p)
    print(f"The pattern {p} exists in {s} at {position} position")
else:
    print("The pattern doesn't exist")

