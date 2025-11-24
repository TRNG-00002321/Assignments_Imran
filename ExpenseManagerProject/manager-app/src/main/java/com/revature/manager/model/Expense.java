package com.revature.manager.model;

public class Expense {
    private final String id;
    private final String userId;
    private final String username;
    private final double amount;
    private final String description;
    private final String date;
    private final String status;
    private final String reviewer;
    private final String comment;
    private final String reviewDate;

    public Expense(
        String id,
        String userId,
        String username,
        double amount,
        String description,
        String date,
        String status,
        String reviewer,
        String comment,
        String reviewDate
    ) {
        this.id = id;
        this.userId = userId;
        this.username = username;
        this.amount = amount;
        this.description = description;
        this.date = date;
        this.status = status;
        this.reviewer = reviewer;
        this.comment = comment;
        this.reviewDate = reviewDate;
    }

    public String getId() {
        return id;
    }

    public String getUserId() {
        return userId;
    }

    public String getUsername() {
        return username;
    }

    public double getAmount() {
        return amount;
    }

    public String getDescription() {
        return description;
    }

    public String getDate() {
        return date;
    }

    public String getStatus() {
        return status;
    }

    public String getReviewer() {
        return reviewer;
    }

    public String getComment() {
        return comment;
    }

    public String getReviewDate() {
        return reviewDate;
    }
}
