import sys


def get_drink_price():
    print("Welcome to the Vending Machine")
    print("1. Water = $1.00")
    print("2. Cola = $1.50")
    print("3. Gatorade = $2.00")

    choice = int(input("Enter your choice (1, 2, or 3): "))

    if choice == 1:
        return 1.00
    elif choice == 2:
        return 1.50
    elif choice == 3:
        return 2.00
    else:
        print("Invalid selection. Exiting program.")
        sys.exit()


def get_coins():
    quarters = int(input("Enter number of quarters: "))
    dimes = int(input("Enter number of dimes: "))
    nickels = int(input("Enter number of nickels: "))
    pennies = int(input("Enter number of pennies: "))

    total = (quarters * 0.25) + (dimes * 0.10) + (nickels * 0.05) + (pennies * 0.01)
    return total


def calculate_change(price, total):
    if total >= price:
        change = total - price
        print("Thank you! Your change is $%.2f" % change)
    else:
        print("Insufficient funds. Please try again.")


def main():
    price = get_drink_price()
    total = get_coins()
    calculate_change(price, total)


# Run the program
main()
