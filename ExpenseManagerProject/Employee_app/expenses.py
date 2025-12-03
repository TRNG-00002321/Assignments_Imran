import logging

import auth
import db

logger = logging.getLogger(__name__)


def get_current_user_expenses(status=None):
    expenses = db.list_expenses_by_user(auth.CURRENT_USER_ID, status=status)
    logger.debug("Found %d expenses for user %s (status=%s)", len(expenses), auth.CURRENT_USER_ID, status)
    return expenses


def print_expense_list(expense_list):
    if not expense_list:
        print("\n  >>> No expenses found. <<<")
        return

    print("\n--------------------------------------------------------------------------------------------------------")
    print(f"| {'NUM':<3} | {'ID':<8} | {'Amount':<8} | {'Date':<10} | {'Status':<10} | {'Category':<12} | {'Description':<20} |")
    print("--------------------------------------------------------------------------------------------------------")

    for i, e in enumerate(expense_list, start=1):
        desc_preview = e['description']
        if len(desc_preview) > 20:
            desc_preview = desc_preview[:17] + "..."

        cat_preview = e.get('category') or "Uncategorized"
        if len(cat_preview) > 12:
            cat_preview = cat_preview[:9] + "..."

        print(
            f"| {i:<3} | {e['id'][:8]:<8} | ${e['amount']:<7.2f} | {e['date']:<10} | {e['status']:<10} | {cat_preview:<12} | {desc_preview:<20} |"
        )

    print("--------------------------------------------------------------------------------------------------------")


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

    while True:
        category = input("Enter category (e.g., Travel, Meals, Office): ").strip()
        if category:
            break
        print("Category cannot be empty. Please enter a category.")

    expense_id = db.insert_expense(auth.CURRENT_USER_ID, amount, description, category)

    print(f"\n-> Expense submitted successfully! ID: {expense_id[:8]}")
    logger.info(
        "Submitted new expense %s for user %s amount %.2f",
        expense_id,
        auth.CURRENT_USER_ID,
        amount,
    )


def view_expense_status():
    print("\n--- PENDING EXPENSES ---")
    pending_expenses = get_current_user_expenses(status="pending")
    print_expense_list(pending_expenses)
    logger.info("Displayed %d pending expenses", len(pending_expenses))


def view_history():
    print("\n--- APPROVED/DENIED HISTORY ---")

    history = [
        e for e in get_current_user_expenses()
        if e['status'] in ('approved', 'denied')
    ]

    print_expense_list(history)

    for e in history:
        if e['comment']:
            print(f"   [ID: {e['id'][:8]}] Manager Comment: {e['comment']}")
    logger.info("Displayed history with %d records", len(history))


def edit_or_delete_pending_expense(action):
    pending = get_current_user_expenses(status="pending")

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

    if action == "edit":
        new_amount = None
        new_description = None
        new_category = None

        while True:
            new_amount_input = input(
                f"Enter new amount (current: ${target_expense['amount']:.2f}, leave blank to skip): $"
            ).strip()

            if not new_amount_input:
                break

            try:
                amount_val = float(new_amount_input)
                if amount_val <= 0:
                    print("Amount must be a positive number.")
                    continue
                new_amount = amount_val
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        new_desc = input(
            f"Enter new description (current: {target_expense['description']}, leave blank to skip): "
        ).strip()
        if new_desc:
            new_description = new_desc

        new_cat = input(
            f"Enter new category (current: {target_expense.get('category', 'Uncategorized')}, leave blank to skip): "
        ).strip()
        if new_cat:
            new_category = new_cat

        updated = db.update_pending_expense(
            target_expense['id'],
            auth.CURRENT_USER_ID,
            amount=new_amount,
            description=new_description,
            category=new_category,
        )

        if updated:
            print(f"\n-> Expense {expense_id_prefix} updated successfully.")
            logger.info("Expense %s saved after edit", target_expense['id'])
        else:
            print("\nUpdate failed. Expense may no longer be pending.")
            logger.warning("Expense %s not updated (no longer pending?)", target_expense['id'])

    elif action == "delete":
        if input(f"Are you sure you want to DELETE expense {expense_id_prefix}? (yes/no): ").lower() == "yes":
            deleted = db.delete_pending_expense(target_expense['id'], auth.CURRENT_USER_ID)
            if deleted:
                print(f"\n-> Expense {expense_id_prefix} deleted successfully.")
                logger.info("Expense %s deleted", target_expense['id'])
            else:
                print("\nDeletion failed. Expense may no longer be pending.")
                logger.warning("Expense %s not deleted (no longer pending?)", target_expense['id'])
        else:
            print("Deletion cancelled.")
            logger.info("Deletion cancelled for expense %s", target_expense['id'])
