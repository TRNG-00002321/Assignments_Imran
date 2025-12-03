package com.revature.manager.dao;

import com.revature.manager.db.Database;
import com.revature.manager.model.Expense;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import java.util.logging.Level;
import java.util.logging.Logger;

public class ExpenseDao {
    private static final Logger logger = Logger.getLogger(ExpenseDao.class.getName());
    private final Database database;

    public ExpenseDao(Database database) {
        this.database = database;
    }

    public List<Expense> listPending() {
        String sql = baseExpenseSelect() + " WHERE e.status = 'pending' ORDER BY e.date ASC";
        return queryExpenses(sql);
    }

    public List<Expense> listByUser(String userId) {
        String sql = baseExpenseSelect() + " WHERE e.user_id = ? ORDER BY e.date DESC";
        return queryExpenses(sql, userId);
    }

    public List<Expense> listByStatus(String status) {
        String sql = baseExpenseSelect() + " WHERE e.status = ? ORDER BY e.date DESC";
        return queryExpenses(sql, status);
    }

    public List<Expense> listByCategory(String category) {
        String sql = baseExpenseSelect() + " WHERE lower(e.category) = lower(?) ORDER BY e.date DESC";
        return queryExpenses(sql, category);
    }

    public List<Expense> listByDateRange(String startDateInclusive, String endDateInclusive) {
        String sql = baseExpenseSelect() + " WHERE e.date BETWEEN ? AND ? ORDER BY e.date ASC";
        return queryExpenses(sql, startDateInclusive, endDateInclusive);
    }

    public boolean updateStatus(String expenseId, String status, String reviewer, String comment) {
        String sql = """
            UPDATE expenses
            SET status = ?, reviewer = ?, comment = ?, review_date = ?
            WHERE id = ?
        """;
        String approvalSql = """
            INSERT INTO approvals (id, expense_id, status, reviewer, comment, review_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """;
        try (Connection conn = database.getConnection();
             PreparedStatement updateExpense = conn.prepareStatement(sql);
             PreparedStatement insertApproval = conn.prepareStatement(approvalSql)) {

            conn.setAutoCommit(false);

            String reviewDate = LocalDate.now().toString();
            updateExpense.setString(1, status);
            updateExpense.setString(2, reviewer);
            updateExpense.setString(3, comment);
            updateExpense.setString(4, reviewDate);
            updateExpense.setString(5, expenseId);
            int rows = updateExpense.executeUpdate();

            if (rows == 0) {
                conn.rollback();
                conn.setAutoCommit(true);
                return false;
            }

            insertApproval.setString(1, UUID.randomUUID().toString());
            insertApproval.setString(2, expenseId);
            insertApproval.setString(3, status);
            insertApproval.setString(4, reviewer);
            insertApproval.setString(5, comment);
            insertApproval.setString(6, reviewDate);
            insertApproval.executeUpdate();

            conn.commit();
            conn.setAutoCommit(true);
            return rows > 0;
        } catch (SQLException e) {
            logger.log(Level.SEVERE, "Failed to update expense " + expenseId, e);
            return false;
        }
    }

    private String baseExpenseSelect() {
        return """
            SELECT e.id, e.user_id, e.amount, e.description, e.date, e.status,
                   e.reviewer, e.comment, e.review_date, e.category, u.username
            FROM expenses e
            LEFT JOIN users u ON e.user_id = u.id
        """;
    }

    private List<Expense> queryExpenses(String sql, Object... args) {
        List<Expense> expenses = new ArrayList<>();
        try (Connection conn = database.getConnection(); PreparedStatement ps = conn.prepareStatement(sql)) {
            for (int i = 0; i < args.length; i++) {
                ps.setObject(i + 1, args[i]);
            }
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    expenses.add(mapExpense(rs));
                }
            }
        } catch (SQLException e) {
            logger.log(Level.SEVERE, "Error querying expenses", e);
        }
        return expenses;
    }

    private Expense mapExpense(ResultSet rs) throws SQLException {
        return new Expense(
            rs.getString("id"),
            rs.getString("user_id"),
            rs.getString("username"),
            rs.getString("category"),
            rs.getDouble("amount"),
            rs.getString("description"),
            rs.getString("date"),
            rs.getString("status"),
            rs.getString("reviewer"),
            rs.getString("comment"),
            rs.getString("review_date")
        );
    }
}
