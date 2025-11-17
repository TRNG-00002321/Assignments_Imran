package com.bank;

public class CheckingAccount extends BankAccount {
    private static final double SURCHARGE_RATE = 0.0001;

    public CheckingAccount(String accountId, String accountName, double balance) {
        super(accountId, accountName, balance);
    }

    @Override
    public void withdraw(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Withdrawal amount cannot be negative or zero.");
        }

        double surcharge = amount * SURCHARGE_RATE;
        double totalWithdrawal = amount + surcharge;

        if (this.balance >= totalWithdrawal) {
            this.balance -= totalWithdrawal;
            System.out.printf("Checking Withdrawal: $%.2f (Surcharge: $%.4f). Remaining balance: $%.2f%n",
                    amount, surcharge, this.balance);
        } else {
            System.out.printf("Insufficient funds. Needed $%.2f (including surcharge) to withdraw $%.2f.%n",
                    totalWithdrawal, amount);
        }
    }

    @Override
    public void applyInterest() {
        // Checking accounts typically don't earn standard interest,
        // but the method is here to satisfy the abstract parent class requirement.
        System.out.println("No standard interest applied to Checking Account.");
    }
}