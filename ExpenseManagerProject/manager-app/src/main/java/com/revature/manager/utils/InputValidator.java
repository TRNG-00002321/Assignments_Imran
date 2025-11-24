package com.revature.manager.utils;

import com.revature.manager.exceptions.ValidationException;

public class InputValidator {
    private InputValidator() {
    }

    public static void requireNonEmpty(String value, String field) {
        if (value == null || value.isBlank()) {
            throw new ValidationException(field + " cannot be empty");
        }
    }

    public static void requireStatus(String status) {
        if (!status.matches("pending|approved|denied")) {
            throw new ValidationException("Status must be pending, approved, or denied");
        }
    }
}
