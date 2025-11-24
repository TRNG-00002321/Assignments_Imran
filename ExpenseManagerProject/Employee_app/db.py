import logging
import sqlite3

DB_FILE = 'revature_expense_manager.db'

logger = logging.getLogger(__name__)
USERS = []
EXPENSES = []


def init_db():
    logger.debug("Ensuring database schema exists in %s", DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            reviewer TEXT,
            comment TEXT,
            review_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)

    conn.commit()
    conn.close()
    logger.debug("Database schema ensured")


def load_data():
    global USERS, EXPENSES

    init_db()

    try:
        logger.info("Loading data from %s", DB_FILE)
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        cur.execute("SELECT id, username, password, role FROM users")
        rows = cur.fetchall()
        USERS = [
            {
                'id': row[0],
                'username': row[1],
                'password': row[2],
                'role': row[3],
            }
            for row in rows
        ]

        cur.execute("""
            SELECT id, user_id, amount, description, date, status, reviewer, comment, review_date
            FROM expenses
        """)
        rows = cur.fetchall()
        EXPENSES = [
            {
                'id': row[0],
                'user_id': row[1],
                'amount': row[2],
                'description': row[3],
                'date': row[4],
                'status': row[5],
                'reviewer': row[6],
                'comment': row[7],
                'review_date': row[8],
            }
            for row in rows
        ]

        conn.close()

        logger.info("Loaded %d users and %d expenses", len(USERS), len(EXPENSES))
        if not USERS:
            logger.warning("No users found in the database. Populate the users table manually.")

    except sqlite3.Error as e:
        logger.exception("Error reading %s: %s", DB_FILE, e)
        USERS = []
        EXPENSES = []


def save_data():
    try:
        logger.info("Saving data to %s", DB_FILE)
        conn = sqlite3.connect(DB_FILE)
        cur = conn.cursor()

        cur.execute("DELETE FROM users")
        for u in USERS:
            cur.execute("""
                INSERT OR REPLACE INTO users (id, username, password, role)
                VALUES (?, ?, ?, ?)
            """, (u['id'], u['username'], u['password'], u['role']))

        cur.execute("DELETE FROM expenses")
        for e in EXPENSES:
            cur.execute("""
                INSERT OR REPLACE INTO expenses
                    (id, user_id, amount, description, date, status, reviewer, comment, review_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                e['id'],
                e['user_id'],
                e['amount'],
                e['description'],
                e['date'],
                e['status'],
                e['reviewer'],
                e['comment'],
                e['review_date'],
            ))

        conn.commit()
        conn.close()
        logger.info("Data saved successfully to %s", DB_FILE)

    except sqlite3.Error as e:
        logger.exception("Error saving data to %s: %s", DB_FILE, e)
