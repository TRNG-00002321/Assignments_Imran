package com.revature.manager.dao;

import com.revature.manager.db.Database;
import com.revature.manager.model.User;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Optional;
import java.util.logging.Level;
import java.util.logging.Logger;

public class UserDao {
    private static final Logger logger = Logger.getLogger(UserDao.class.getName());
    private final Database database;

    public UserDao(Database database) {
        this.database = database;
    }

    public Optional<User> findByUsername(String username) {
        String sql = "SELECT id, username, password, role FROM users WHERE username = ?";
        try (Connection conn = database.getConnection(); PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, username);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return Optional.of(mapUser(rs));
                }
            }
        } catch (SQLException e) {
            logger.log(Level.SEVERE, "Error looking up user " + username, e);
        }
        return Optional.empty();
    }

    private User mapUser(ResultSet rs) throws SQLException {
        return new User(
            rs.getString("id"),
            rs.getString("username"),
            rs.getString("password"),
            rs.getString("role")
        );
    }
}
