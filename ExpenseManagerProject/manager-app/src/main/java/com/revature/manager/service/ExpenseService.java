package com.revature.manager.service;

import com.revature.manager.dao.ExpenseDao;
import com.revature.manager.dao.UserDao;
import com.revature.manager.model.Expense;
import com.revature.manager.model.User;

import java.util.List;
import java.util.Optional;
import java.util.logging.Logger;

public class ExpenseService {
    private static final Logger logger = Logger.getLogger(ExpenseService.class.getName());

    private final ExpenseDao expenseDao;
    private final UserDao userDao;

    public ExpenseService(ExpenseDao expenseDao, UserDao userDao) {
        this.expenseDao = expenseDao;
        this.userDao = userDao;
    }

    public List<Expense> getPendingExpenses() {
        return expenseDao.listPending();
    }

    public boolean approveExpense(String expenseId, User reviewer, String comment) {
        boolean updated = expenseDao.updateStatus(expenseId, "approved", reviewer.getUsername(), comment);
        if (updated) {
            logger.info("Approved expense " + expenseId + " by " + reviewer.getUsername());
        }
        return updated;
    }

    public boolean denyExpense(String expenseId, User reviewer, String comment) {
        boolean updated = expenseDao.updateStatus(expenseId, "denied", reviewer.getUsername(), comment);
        if (updated) {
            logger.info("Denied expense " + expenseId + " by " + reviewer.getUsername());
        }
        return updated;
    }

    public List<Expense> listExpensesByUser(String userId) {
        return expenseDao.listByUser(userId);
    }

    public List<Expense> listExpensesByStatus(String status) {
        return expenseDao.listByStatus(status);
    }

    public Optional<User> findUserByUsername(String username) {
        return userDao.findByUsername(username);
    }
}
