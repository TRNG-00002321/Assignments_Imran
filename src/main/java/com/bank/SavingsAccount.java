package com.bank;

public class SavingsAccount extends BankAccount {
    private static final double INTEREST_RATE = 0.05;
    private static final double MIN_WITHDRAWABLE_BALANCE = 5000.00;

    public SavingsAccount(String accountId, String accountName, double balance) {
        super(accountId, accountName, balance);
    }

    @Override
    public void withdraw(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdrawal amount cannot be negative or zero.");
        }

        // Check for minimum balance restriction
        if (this.balance < MIN_WITHDRAWABLE_BALANCE) {
            System.out.println("Transaction Failed: Savings account balance must be at least $" + MIN_WITHDRAWABLE_BALANCE + " to withdraw.");
            return;
        }

        if (this.balance >= amount) {
            this.balance -= amount;
            System.out.printf("Savings Withdrawal: $%.2f. Remaining balance: $%.2f%n", amount, this.balance);
        } else {
            System.out.println("Insufficient funds for withdrawal of $" + amount);
        }
    }

    @Override
    public void applyInterest() {
        double interest = this.balance * INTEREST_RATE;
        this.balance += interest;
        System.out.printf("Interest applied (5%%): $%.2f. New balance: $%.2f%n", interest, this.balance);
    }
}