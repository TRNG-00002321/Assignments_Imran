package com.revature.manager.ui;

import com.revature.manager.model.Expense;
import com.revature.manager.model.User;
import com.revature.manager.service.AuthService;
import com.revature.manager.service.ExpenseService;
import com.revature.manager.utils.InputValidator;
import com.revature.manager.exceptions.ValidationException;

import java.util.List;
import java.util.Optional;
import java.util.Scanner;
import java.util.logging.Logger;

public class Menu {
    private static final Logger logger = Logger.getLogger(Menu.class.getName());

    private final AuthService authService;
    private final ExpenseService expenseService;

    public Menu(AuthService authService, ExpenseService expenseService) {
        this.authService = authService;
        this.expenseService = expenseService;
    }

    public void start() {
        try (Scanner scanner = new Scanner(System.in)) {
            Optional<User> managerOpt = authService.login(scanner);
            if (managerOpt.isEmpty()) {
                return;
            }
            User manager = managerOpt.get();

            boolean running = true;
            while (running) {
                printMenu();
                String choice = scanner.nextLine().trim();
                switch (choice) {
                    case "1" -> showPending();
                    case "2" -> updateExpense(scanner, manager, true);
                    case "3" -> updateExpense(scanner, manager, false);
                    case "4" -> reportByUser(scanner);
                    case "5" -> reportByStatus(scanner);
                    case "6" -> running = false;
                    default -> System.out.println("Invalid choice. Try again.");
                }
            }
        }
    }

    private void printMenu() {
        System.out.println("\n--- Manager Menu ---");
        System.out.println("1. View Pending Expenses");
        System.out.println("2. Approve an Expense");
        System.out.println("3. Deny an Expense");
        System.out.println("4. Report by User");
        System.out.println("5. Report by Status");
        System.out.println("6. Exit");
        System.out.print("Enter choice: ");
    }

    private void showPending() {
        List<Expense> pending = expenseService.getPendingExpenses();
        if (pending.isEmpty()) {
            System.out.println("\nNo pending expenses.");
            return;
        }
        printExpenses(pending, true);
    }

    private void updateExpense(Scanner scanner, User manager, boolean approve) {
        List<Expense> pending = expenseService.getPendingExpenses();
        if (pending.isEmpty()) {
            System.out.println("\nNo pending expenses to review.");
            return;
        }
        printExpenses(pending, true);
        System.out.print("\nEnter expense number to " + (approve ? "approve" : "deny") + ": ");
        String input = scanner.nextLine().trim();
        int index;
        try {
            index = Integer.parseInt(input) - 1;
        } catch (NumberFormatException e) {
            System.out.println("Invalid number.");
            return;
        }
        if (index < 0 || index >= pending.size()) {
            System.out.println("Selection out of range.");
            return;
        }

        Expense target = pending.get(index);
        System.out.print("Add a comment (optional): ");
        String comment = scanner.nextLine().trim();

        boolean success = approve
            ? expenseService.approveExpense(target.getId(), manager, comment)
            : expenseService.denyExpense(target.getId(), manager, comment);

        if (success) {
            System.out.println("Expense " + target.getId() + " updated successfully.");
        } else {
            System.out.println("Failed to update expense.");
        }
    }

    private void reportByUser(Scanner scanner) {
        System.out.print("\nEnter username to report on: ");
        String username = scanner.nextLine().trim();
        Optional<User> userOpt = expenseService.findUserByUsername(username);
        if (userOpt.isEmpty()) {
            System.out.println("User not found.");
            return;
        }
        List<Expense> expenses = expenseService.listExpensesByUser(userOpt.get().getId());
        if (expenses.isEmpty()) {
            System.out.println("No expenses found for " + username + ".");
            return;
        }
        printExpenses(expenses, false);
    }

    private void reportByStatus(Scanner scanner) {
        System.out.print("\nEnter status (pending/approved/denied): ");
        String status = scanner.nextLine().trim().toLowerCase();
        try {
            InputValidator.requireStatus(status);
            List<Expense> expenses = expenseService.listExpensesByStatus(status);
            if (expenses.isEmpty()) {
                System.out.println("No expenses found with status " + status + ".");
                return;
            }
            printExpenses(expenses, false);
        } catch (ValidationException e) {
            System.out.println(e.getMessage());
        }
    }

    private void printExpenses(List<Expense> expenses, boolean showIndex) {
        String line = "--------------------------------------------------------------------------------------------------------------";
        System.out.println("\n" + line);
        System.out.printf(
            "| %3s | %-8s | %-10s | %-10s | %-10s | %-10s | %-20s | %-15s |%n",
            showIndex ? "NUM" : "",
            "ID",
            "User",
            "Amount",
            "Date",
            "Status",
            "Description",
            "Comment"
        );
        System.out.println(line);
        int i = 1;
        for (Expense e : expenses) {
            String comment = e.getComment() != null ? truncate(e.getComment(), 15) : "-";
            String userLabel = e.getUsername() != null ? e.getUsername() : e.getUserId();
            System.out.printf(
                "| %3s | %-8s | %-10s | $%-8.2f | %-10s | %-10s | %-20s | %-15s |%n",
                showIndex ? i : "",
                e.getId().substring(0, Math.min(8, e.getId().length())),
                userLabel,
                e.getAmount(),
                e.getDate(),
                e.getStatus(),
                truncate(e.getDescription(), 20),
                comment
            );
            i++;
        }
        System.out.println(line);
        logger.info("Displayed " + expenses.size() + " expense rows");
    }

    private String truncate(String value, int maxLen) {
        if (value == null || value.isEmpty()) {
            return "-";
        }
        return value.length() <= maxLen ? value : value.substring(0, maxLen - 3) + "...";
    }
}
