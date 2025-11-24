import logging
import time
import uuid

import auth
import db

logger = logging.getLogger(__name__)


def get_current_user_expenses():
    user_expenses = []
    for expense in db.EXPENSES:
        if expense['user_id'] == auth.CURRENT_USER_ID:
            user_expenses.append(expense)
    logger.debug("Found %d expenses for user %s", len(user_expenses), auth.CURRENT_USER_ID)
    return user_expenses


def print_expense_list(expense_list):
    if not expense_list:
        print("\n  >>> No expenses found. <<<")
        return

    print("\n----------------------------------------------------------------------------------")
    print(f"| {'NUM':<3} | {'ID':<8} | {'Amount':<8} | {'Date':<10} | {'Status':<10} | {'Description':<20} |")
    print("----------------------------------------------------------------------------------")

    for i in range(len(expense_list)):
        e = expense_list[i]
        index = i + 1

        desc_preview = e['description']
        if len(desc_preview) > 20:
            desc_preview = desc_preview[:17] + '...'

        print(f"| {index:<3} | {e['id'][:8]:<8} | ${e['amount']:<7.2f} | {e['date']:<10} | {e['status']:<10} | {desc_preview:<20} |")

    print("----------------------------------------------------------------------------------")


def submit_new_expense():
    while True:
        try:
            amount_input = input("Enter expense amount (e.g., 50.00): $")
            if not amount_input:
                print("Amount cannot be empty.")
                continue

            amount = float(amount_input)
            if amount <= 0:
                print("Amount must be a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number (e.g., 50.00).")

    while True:
        description = input("Enter description (e.g., Office Supplies): ").strip()
        if description:
            break
        print("Description cannot be empty. Please enter a description.")

    new_expense = {
        'id': str(uuid.uuid4()),
        'user_id': auth.CURRENT_USER_ID,
        'amount': amount,
        'description': description,
        'date': time.strftime("%Y-%m-%d"),
        'status': 'pending',
        'reviewer': None,
        'comment': None,
        'review_date': None,
    }

    db.EXPENSES.append(new_expense)
    print(f"\n✅ Expense submitted successfully! ID: {new_expense['id'][:8]}")
    logger.info(
        "Submitted new expense %s for user %s amount %.2f",
        new_expense['id'],
        auth.CURRENT_USER_ID,
        amount,
    )


def view_expense_status():
    print("\n--- PENDING EXPENSES ---")

    pending_expenses = []
    for expense in get_current_user_expenses():
        if expense['status'] == 'pending':
            pending_expenses.append(expense)

    print_expense_list(pending_expenses)
    logger.info("Displayed %d pending expenses", len(pending_expenses))


def view_history():
    print("\n--- APPROVED/DENIED HISTORY ---")

    history = []
    for expense in get_current_user_expenses():
        if expense['status'] in ('approved', 'denied'):
            history.append(expense)

    print_expense_list(history)

    for e in history:
        if e['comment']:
            print(f"   [ID: {e['id'][:8]}] Manager Comment: {e['comment']}")
    logger.info("Displayed history with %d records", len(history))


def edit_or_delete_pending_expense(action):
    pending = []
    for expense in get_current_user_expenses():
        if expense['status'] == 'pending':
            pending.append(expense)

    if not pending:
        print("\nNo pending expenses to modify.")
        logger.info("No pending expenses available to %s for user %s", action, auth.CURRENT_USER_ID)
        return

    print_expense_list(pending)

    target_expense = None
    while True:
        seq_input = input(f"\nEnter the sequence number (NUM) to {action}: ").strip()
        try:
            seq_num = int(seq_input)
            if 1 <= seq_num <= len(pending):
                target_expense = pending[seq_num - 1]
                break
            else:
                print(f"Invalid number. Please enter a number between 1 and {len(pending)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    expense_id_prefix = target_expense['id'][:8]

    if action == 'edit':
        while True:
            new_amount_input = input(
                f"Enter new amount (current: ${target_expense['amount']:.2f}, leave blank to skip): $"
            ).strip()

            if not new_amount_input:
                break

            try:
                new_amount = float(new_amount_input)
                if new_amount <= 0:
                    print("Amount must be a positive number.")
                    continue
                target_expense['amount'] = new_amount
                logger.info(
                    "Updated amount for expense %s to %.2f", target_expense['id'], new_amount
                )
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        while True:
            new_desc = input(
                f"Enter new description (current: {target_expense['description']}, leave blank to skip): "
            ).strip()

            if not new_desc:
                break

            target_expense['description'] = new_desc
            logger.info("Updated description for expense %s", target_expense['id'])
            break

        print(f"\n✅ Expense {expense_id_prefix} updated successfully.")
        db.save_data()
        logger.info("Expense %s saved after edit", target_expense['id'])

    elif action == 'delete':
        if input(f"Are you sure you want to DELETE expense {expense_id_prefix}? (yes/no): ").lower() == 'yes':
            db.EXPENSES.remove(target_expense)

            print(f"\n✅ Expense {expense_id_prefix} deleted successfully.")
            db.save_data()
            logger.info("Expense %s deleted", target_expense['id'])
        else:
            print("Deletion cancelled.")
            logger.info("Deletion cancelled for expense %s", target_expense['id'])
