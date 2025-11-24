package com.revature.manager.exceptions;

public class ValidationException extends RuntimeException {
    public ValidationException(String message) {
        super(message);
    }
}
