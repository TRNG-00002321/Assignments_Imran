import csv
import os
from datetime import datetime

# --- Configuration ---
CSV_FILE = 'expenses.csv'
FIELDNAMES = ['id', 'date', 'amount', 'category', 'description']

# --- Helper Functions ---

def ensure_csv_exists():
    """Checks if the CSV file exists and creates it with headers if it doesn't."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def load_expenses():
    """Loads all expenses from the CSV file into a list of dictionaries."""
    ensure_csv_exists()
    expenses = []
    try:
        with open(CSV_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert amount back to float immediately
                try:
                    row['amount'] = float(row['amount'])
                    expenses.append(row)
                except ValueError:
                    # Basic error note
                    print(f"Skipped a row with invalid amount: {row}")
        return expenses
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def save_expenses(expenses):
    """Writes the current list of expenses to the CSV file, overwriting the old data."""
    try:
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            for expense in expenses:
                # Need to convert amount back to string for saving
                expense_to_write = expense.copy()
                expense_to_write['amount'] = str(expense['amount'])
                writer.writerow(expense_to_write)
        print("Data saved.")
    except Exception as e:
        print(f"Error writing file: {e}")

# --- Validation Functions (Very Basic) ---

def get_valid_date(prompt):
    """Gets date input and checks format."""
    while True:
        date_str = input(prompt).strip()
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD format.")

def get_valid_amount(prompt):
    """Gets amount input and checks if it's a non-negative number."""
    while True:
        amount_str = input(prompt).strip()
        try:
            amount = float(amount_str)
            if amount >= 0:
                return amount
            else:
                print("Amount must be non-negative.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# --- Core Features ---

def get_next_id(expenses):
    """Generates the next sequential ID (simple approach)."""
    max_id = 0
    for expense in expenses:
        try:
            current_id = int(expense['id'])
            if current_id > max_id:
                max_id = current_id
        except ValueError:
            # Ignore non-numeric IDs if they somehow appear
            pass
    return max_id + 1

def add_expense():
    """Allows the user to add a new expense."""
    print("\n--- Add Expense ---")

    expenses = load_expenses()

    # Input with validation
    date_input = get_valid_date("Date (YYYY-MM-DD): ")
    amount = get_valid_amount("Amount: ")
    category = input("Category: ").strip()
    description = input("Description (optional): ").strip()

    new_id = str(get_next_id(expenses))

    new_expense = {
        'id': new_id,
        'date': date_input,
        'amount': amount,
        'category': category,
        'description': description
    }

    expenses.append(new_expense)
    save_expenses(expenses)
    print(f"\nExpense added with ID: {new_id}")

def view_expenses():
    """Displays all expenses in a simple list."""
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\n--- All Expenses ---")

    # Print simple header
    print(f"{'ID':<4} | {'Date':<10} | {'Amount':<8} | {'Category':<15} | Description")
    print("-" * 60)

    for expense in expenses:
        # Format the amount to two decimal places for display
        display_amount = f"{expense['amount']:.2f}"
        print(
            f"{expense['id']:<4} | "
            f"{expense['date']:<10} | "
            f"{display_amount:<8} | "
            f"{expense['category']:<15} | "
            f"{expense['description']}"
        )

def delete_expense():
    """Deletes an expense by ID."""
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses to delete.")
        return

    expense_id = input("\nEnter the ID to delete: ").strip()

    found = False
    new_expenses = []

    # Simple list filtering logic (using a loop instead of list comprehension)
    for expense in expenses:
        if expense['id'] == expense_id:
            found = True
            # Skip adding this expense to the new list
        else:
            new_expenses.append(expense)

    if found:
        save_expenses(new_expenses)
        print(f"\nExpense ID {expense_id} deleted.")
    else:
        print(f"\nError: ID {expense_id} not found.")

def edit_expense():
    """Edits an existing expense by ID."""
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses to edit.")
        return

    expense_id = input("\nEnter the ID of the expense to edit: ").strip()

    expense_to_edit = None

    # Simple linear search
    for expense in expenses:
        if expense['id'] == expense_id:
            expense_to_edit = expense
            break

    if expense_to_edit is None:
        print(f"\nError: ID {expense_id} not found.")
        return

    print(f"\nEditing Expense ID: {expense_to_edit['id']}")

    # Get new values, allowing blank to keep old value

    new_date = input(f"New date ({expense_to_edit['date']}) or leave blank: ").strip()
    if new_date:
        # Re-using the validation logic
        if datetime.strptime(new_date, '%Y-%m-%d'):
            expense_to_edit['date'] = new_date
        else:
            print("Date not updated (invalid format).")

    new_amount_str = input(f"New amount ({expense_to_edit['amount']:.2f}) or leave blank: ").strip()
    if new_amount_str:
        if get_valid_amount(f"Amount '{new_amount_str}' is invalid, re-enter: ") != None: # Simple check
            expense_to_edit['amount'] = float(new_amount_str)

    new_category = input(f"New category ({expense_to_edit['category']}) or leave blank: ").strip()
    if new_category:
        expense_to_edit['category'] = new_category

    new_description = input(f"New description ({expense_to_edit['description']}) or leave blank: ").strip()
    if new_description:
        expense_to_edit['description'] = new_description

    # Since we modified the dictionary directly, we just save the whole list
    save_expenses(expenses)
    print(f"\nExpense ID {expense_id} updated.")

# --- Summary Feature ---

def show_summary():
    """Calculates and displays summary statistics."""
    expenses = load_expenses()
    if not expenses:
        print("\nNo expenses recorded.")
        return

    print("\n--- Summary ---")

    # 1. Total Expenses (All Time)
    total_all_time = 0.0
    for expense in expenses:
        total_all_time += expense['amount']
    print(f"Total Expenses (All Time): ${total_all_time:.2f}")

    # 2. Total by Category
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    print("\nTotal by Category:")
    for category, total in category_totals.items():
        print(f"  - {category}: ${total:.2f}")

    # 3. Total for a Date Range
    print("\n--- Date Range Summary ---")
    start_date = get_valid_date("Enter Start Date (YYYY-MM-DD): ")
    end_date = get_valid_date("Enter End Date (YYYY-MM-DD): ")

    # Convert input strings to datetime objects for comparison
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')

    range_total = 0.0

    for expense in expenses:
        expense_dt = datetime.strptime(expense['date'], '%Y-%m-%d')

        # Check if expense date is between or equal to start/end dates
        if start_dt <= expense_dt <= end_dt:
            range_total += expense['amount']

    print(f"Total between {start_date} and {end_date}: ${range_total:.2f}")

# --- assignments.switch_practice Application ---

def print_menu():
    """Displays the main menu options."""
    print("\n--- Expense Tracker ---")
    print("A: Add Expense")
    print("V: View All Expenses")
    print("E: Edit Expense")
    print("D: Delete Expense")
    print("S: Show Summaries")
    print("Q: Quit")
    print("-" * 25)

def main():
    """The main application loop."""
    ensure_csv_exists()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip().upper()

        if choice == 'A':
            add_expense()
        elif choice == 'V':
            view_expenses()
        elif choice == 'E':
            edit_expense()
        elif choice == 'D':
            delete_expense()
        elif choice == 'S':
            show_summary()
        elif choice == 'Q':
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()