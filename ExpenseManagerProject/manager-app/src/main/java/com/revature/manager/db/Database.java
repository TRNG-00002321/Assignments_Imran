package com.revature.manager.db;

import java.nio.file.Path;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Database {
    private static final Logger logger = Logger.getLogger(Database.class.getName());

    private final Path dbPath;
    private final String jdbcUrl;

    public Database(Path dbPath) {
        this.dbPath = dbPath;
        this.jdbcUrl = "jdbc:sqlite:" + dbPath.toAbsolutePath();
    }

    public Path getDbPath() {
        return dbPath;
    }

    public Connection getConnection() throws SQLException {
        return DriverManager.getConnection(jdbcUrl);
    }

    public void initSchema() {
        try (Connection conn = getConnection(); Statement stmt = conn.createStatement()) {
            stmt.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                );
            """);

            stmt.execute("""
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
            """);

            logger.info("Database schema verified at " + dbPath.toAbsolutePath());
        } catch (SQLException e) {
            logger.log(Level.SEVERE, "Failed to initialize schema", e);
        }
    }

}
