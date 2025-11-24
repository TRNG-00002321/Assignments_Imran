import logging

import db

logger = logging.getLogger(__name__)

CURRENT_USER = None
CURRENT_USER_ID = None


def login():
    global CURRENT_USER, CURRENT_USER_ID

    if not db.USERS:
        print("\nFATAL ERROR: No user accounts found in database. Cannot log in.")
        logger.error("Login failed: no users found in database")
        return False

    print("\n--- Employee Login ---")

    username = input("Username: ").strip()
    logger.info("Login attempt for username %s", username)

    target_user = None
    for user in db.USERS:
        if user['username'] == username:
            target_user = user
            break

    if target_user is None:
        print("Login failed: Username incorrect or user not found.")
        logger.warning("Login failed: user %s not found", username)
        return False

    if target_user['role'] != 'Employee':
        print("Login failed: Account found, but access restricted (Role is not Employee).")
        logger.warning("Login failed: user %s has role %s", username, target_user['role'])
        return False

    max_attempts = 3
    for attempt in range(max_attempts):
        password = input("Password: ").strip()

        if target_user['password'] == password:
            CURRENT_USER = target_user['username']
            CURRENT_USER_ID = target_user['id']
            print(f"\nWelcome, {CURRENT_USER}!")
            logger.info("Login successful for user %s", CURRENT_USER)
            return True
        else:
            remaining = max_attempts - (attempt + 1)
            if remaining > 0:
                print(f"Password incorrect. You have {remaining} attempts remaining.")
                logger.warning(
                    "Password attempt failed for user %s (%d/%d)",
                    username,
                    attempt + 1,
                    max_attempts,
                )
            else:
                print("Password incorrect. Max attempts reached. Returning to main menu.")
                logger.error("Login failed: max attempts reached for user %s", username)
                return False

    return False
