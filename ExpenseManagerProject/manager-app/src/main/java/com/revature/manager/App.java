package com.revature.manager;

import com.revature.manager.dao.ExpenseDao;
import com.revature.manager.dao.UserDao;
import com.revature.manager.db.Database;
import com.revature.manager.service.AuthService;
import com.revature.manager.service.ExpenseService;
import com.revature.manager.ui.Menu;

import java.io.IOException;
import java.nio.file.Path;
import java.util.logging.ConsoleHandler;
import java.util.logging.FileHandler;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.logging.SimpleFormatter;

public class App {
    private static final Logger logger = Logger.getLogger(App.class.getName());
    private static final String DEFAULT_DB = "revature_expense_manager.db";
    private static final String LOG_FILE = "manager_app.log";

    private static void configureLogging() {
        Logger root = Logger.getLogger("");
        root.setLevel(Level.INFO);
        for (var handler : root.getHandlers()) {
            root.removeHandler(handler);
        }
        try {
            FileHandler fileHandler = new FileHandler(LOG_FILE, true);
            fileHandler.setFormatter(new SimpleFormatter());
            fileHandler.setLevel(Level.INFO);
            root.addHandler(fileHandler);
        } catch (IOException e) {
            logger.log(Level.SEVERE, "Failed to initialize file logging", e);
        }

        ConsoleHandler consoleHandler = new ConsoleHandler();
        consoleHandler.setFormatter(new SimpleFormatter());
        consoleHandler.setLevel(Level.WARNING);
        root.addHandler(consoleHandler);
    }

    public static void main(String[] args) {
        configureLogging();

        Path dbPath = resolveDbPath();
        Database database = new Database(dbPath);
        database.initSchema();

        UserDao userDao = new UserDao(database);
        ExpenseDao expenseDao = new ExpenseDao(database);

        AuthService authService = new AuthService(userDao);
        ExpenseService expenseService = new ExpenseService(expenseDao, userDao);
        Menu menu = new Menu(authService, expenseService);

        logger.info("Launching Manager App using database at " + database.getDbPath());
        menu.start();
        logger.info("Manager App shut down");
    }

    private static Path resolveDbPath() {
        String env = System.getenv("EXPENSE_DB_FILE");
        if (env != null && !env.isBlank()) {
            return Path.of(env);
        }
        Path local = Path.of(DEFAULT_DB);
        if (local.toFile().exists()) {
            return local;
        }
        Path parent = Path.of("..", DEFAULT_DB);
        if (parent.toFile().exists()) {
            return parent;
        }
        return local;
    }
}
