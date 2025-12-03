package com.revature.manager.utils;

import com.revature.manager.exceptions.ValidationException;

import java.time.LocalDate;
import java.time.format.DateTimeParseException;

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

    public static LocalDate parseIsoDate(String value, String field) {
        try {
            return LocalDate.parse(value);
        } catch (DateTimeParseException e) {
            throw new ValidationException(field + " must be in YYYY-MM-DD format");
        }
    }
}
