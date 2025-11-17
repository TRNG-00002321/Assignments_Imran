package com.bank;

public abstract class BankAccount {
    protected String accountId;
    protected String accountName;
    protected double balance;

    public BankAccount(String accountId, String accountName, double balance) {
        this.accountId = accountId;
        this.accountName = accountName;
        this.balance = balance;
    }

    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Deposit amount cannot be negative or zero.");
        }
        this.balance += amount;
        System.out.printf("Deposited $%.2f. New balance: $%.2f%n", amount, this.balance);
    }

    // Abstract methods remain
    public abstract void withdraw(double amount);
    public abstract void applyInterest(); // Added this to abstract base class for consistency

    public void displayAccountInfo() {
        System.out.println("---------------------------------");
        System.out.println("Account Type: " + this.getClass().getSimpleName());
        System.out.println("ID: " + accountId);
        System.out.println("Name: " + accountName);
        System.out.printf("Current Balance: $%.2f%n", balance);
        System.out.println("---------------------------------");
    }
}