import logging
import os
import sqlite3
import uuid
from datetime import date

DB_FILE = os.getenv('EXPENSE_DB_FILE', 'revature_expense_manager.db')

logger = logging.getLogger(__name__)


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    logger.debug("Ensuring database schema exists in %s", DB_FILE)
    conn = get_connection()
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
            category TEXT NOT NULL,
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

    try:
        cur.execute("ALTER TABLE expenses ADD COLUMN category TEXT DEFAULT 'Uncategorized'")
    except sqlite3.OperationalError:
        pass

    cur.execute("""
        CREATE TABLE IF NOT EXISTS approvals (
            id TEXT PRIMARY KEY,
            expense_id TEXT NOT NULL,
            status TEXT NOT NULL,
            reviewer TEXT,
            comment TEXT,
            review_date TEXT NOT NULL,
            FOREIGN KEY (expense_id) REFERENCES expenses(id)
        );
    """)

    conn.commit()
    conn.close()
    logger.debug("Database schema ensured")


def users_exist():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    conn.close()
    return count > 0


def get_user_by_username(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, password, role FROM users WHERE LOWER(username) = LOWER(?)",
        (username,),
    )
    row = cur.fetchone()
    conn.close()
    if row:
        return {'id': row[0], 'username': row[1], 'password': row[2], 'role': row[3]}
    return None


def list_expenses_by_user(user_id, status=None):
    conn = get_connection()
    cur = conn.cursor()
    if status:
        cur.execute("""
            SELECT id, user_id, category, amount, description, date, status, reviewer, comment, review_date
            FROM expenses
            WHERE user_id = ? AND status = ?
            ORDER BY date DESC
        """, (user_id, status))
    else:
        cur.execute("""
            SELECT id, user_id, category, amount, description, date, status, reviewer, comment, review_date
            FROM expenses
            WHERE user_id = ?
            ORDER BY date DESC
        """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [
        {
            'id': row[0],
            'user_id': row[1],
            'category': row[2],
            'amount': row[3],
            'description': row[4],
            'date': row[5],
            'status': row[6],
            'reviewer': row[7],
            'comment': row[8],
            'review_date': row[9],
        }
        for row in rows
    ]


def insert_expense(user_id, amount, description, category):
    conn = get_connection()
    cur = conn.cursor()
    expense_id = str(uuid.uuid4())
    cur.execute("""
        INSERT INTO expenses
        (id, user_id, category, amount, description, date, status, reviewer, comment, review_date)
        VALUES (?, ?, ?, ?, ?, ?, 'pending', NULL, NULL, NULL)
    """, (expense_id, user_id, category, amount, description, date.today().isoformat()))
    conn.commit()
    conn.close()
    logger.info("Inserted expense %s for user %s", expense_id, user_id)
    return expense_id


def update_pending_expense(expense_id, user_id, amount=None, description=None, category=None):
    fields = []
    values = []
    if amount is not None:
        fields.append("amount = ?")
        values.append(amount)
    if description is not None:
        fields.append("description = ?")
        values.append(description)
    if category is not None:
        fields.append("category = ?")
        values.append(category)

    if not fields:
        return False

    values.extend([expense_id, user_id])
    sql = f"""
        UPDATE expenses
        SET {", ".join(fields)}
        WHERE id = ? AND user_id = ? AND status = 'pending'
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, tuple(values))
    conn.commit()
    updated = cur.rowcount > 0
    conn.close()
    if updated:
        logger.info("Updated pending expense %s for user %s", expense_id, user_id)
    else:
        logger.warning("No pending expense updated for %s (user %s)", expense_id, user_id)
    return updated


def delete_pending_expense(expense_id, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ? AND status = 'pending'",
        (expense_id, user_id),
    )
    conn.commit()
    deleted = cur.rowcount > 0
    conn.close()
    if deleted:
        logger.info("Deleted pending expense %s for user %s", expense_id, user_id)
    else:
        logger.warning("No pending expense deleted for %s (user %s)", expense_id, user_id)
    return deleted
