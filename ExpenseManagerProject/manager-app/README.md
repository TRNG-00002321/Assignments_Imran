## Manager App (Java)

Console CLI for managers to review, approve, and deny expenses stored in the shared SQLite database.

### Requirements
- Java 17+
- Maven 3+

### Getting started
1. Ensure the shared database file `revature_expense_manager.db` exists at the repo root (or set `EXPENSE_DB_FILE` to a custom path).
2. From this folder build a fat jar and run it:
   ```bash
   mvn clean package
   java -jar target/manager-app-0.1.0-SNAPSHOT-shaded.jar
   ```
   (If the DB is one level up, the app auto-falls back to `../revature_expense_manager.db`. Override with `EXPENSE_DB_FILE` if needed.)
3. Log in with a user whose role is `Manager`.

### Environment
- `EXPENSE_DB_FILE`: path to the SQLite database file (default: `revature_expense_manager.db`).
