import logging

import auth
import db
import menu

LOG_FILE = "employee_app.log"
logger = logging.getLogger(__name__)


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler(LOG_FILE)],
    )


def main():
    configure_logging()
    logger.info("Employee app starting")
    db.load_data()

    while True:
        if db.USERS:
            login_success = auth.login()
            if login_success:
                logger.info("Entering employee menu")
                menu.employee_menu()
            else:
                retry = input("Do you want to try a different username? (yes/no): ").lower()
                if retry != 'yes':
                    logger.info("User declined to retry login; exiting application")
                    break
        else:
            print("\nApplication shutting down. Thank you for using the Employee App.")
            logger.error("Application shutting down due to missing users")
            break
    logger.info("Application exiting")


if __name__ == "__main__":
    main()
