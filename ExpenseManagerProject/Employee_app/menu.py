import logging

import auth
import db
import expenses

logger = logging.getLogger(__name__)


def employee_menu():
    while True:
        print("\n--- Employee App Menu ---")
        print("1. Submit New Expense")
        print("2. View Pending Expenses Status")
        print("3. View Approved/Denied History")
        print("4. Edit Pending Expense")
        print("5. Delete Pending Expense")
        print("6. Logout and Exit")

        choice = input("Enter choice: ").strip()
        logger.info("Menu selection %s by user %s", choice, auth.CURRENT_USER_ID)

        if choice == '1':
            expenses.submit_new_expense()
            db.save_data()
        elif choice == '2':
            expenses.view_expense_status()
        elif choice == '3':
            expenses.view_history()
        elif choice == '4':
            expenses.edit_or_delete_pending_expense('edit')
        elif choice == '5':
            expenses.edit_or_delete_pending_expense('delete')
        elif choice == '6':
            auth.CURRENT_USER = None
            auth.CURRENT_USER_ID = None
            print("\nLogged out. Goodbye!")
            logger.info("User logged out")
            break
        else:
            print("Invalid choice. Please try again.")
            logger.warning("Invalid menu choice %s entered", choice)
