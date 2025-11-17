package com.bank;

import java.util.InputMismatchException;
import java.util.Scanner;

public class BankDemo {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        BankAccount account = null;

        System.out.println("--- Welcome to the Bank Account Setup ---");

        // 1. Account Selection and Initialization
        while (account == null) {
            System.out.print("Enter account type (S for Savings, C for Checking): ");
            String type = scanner.nextLine().trim().toUpperCase();

            System.out.print("Enter Account ID: ");
            String id = scanner.nextLine();

            System.out.print("Enter Account Name: ");
            String name = scanner.nextLine();

            double initialBalance = 0;
            try {
                System.out.print("Enter Initial Balance: ");
                initialBalance = scanner.nextDouble();
                scanner.nextLine(); // Consume newline
            } catch (InputMismatchException e) {
                System.out.println("Invalid input. Balance must be a number.");
                scanner.nextLine(); // Clear buffer
                continue;
            }

            if (initialBalance < 0) {
                System.out.println("Error: Initial balance cannot be negative.");
                continue;
            }

            if (type.equals("S")) {
                account = new SavingsAccount(id, name, initialBalance);
            } else if (type.equals("C")) {
                account = new CheckingAccount(id, name, initialBalance);
            } else {
                System.out.println("Invalid account type selected. Please try again.");
            }
        }

        account.displayAccountInfo();

        // 2. Transaction Loop
        boolean running = true;
        while (running) {
            System.out.println("\n--- Transactions ---");
            System.out.println("1: Deposit | 2: Withdraw | 3: Apply Interest | 4: Display Info | 5: Exit");
            System.out.print("Select option: ");

            String choice = scanner.nextLine().trim();
            double amount = 0;

            try {
                switch (choice) {
                    case "1": // Deposit
                        System.out.print("Enter deposit amount: ");
                        amount = scanner.nextDouble();
                        account.deposit(amount);
                        break;

                    case "2": // Withdraw
                        System.out.print("Enter withdrawal amount: ");
                        amount = scanner.nextDouble();
                        account.withdraw(amount);
                        break;

                    case "3": // Apply Interest
                        account.applyInterest();
                        break;

                    case "4": // Display Info
                        account.displayAccountInfo();
                        break;

                    case "5": // Exit
                        running = false;
                        System.out.println("Thank you for using the Mini Bank Application.");
                        break;

                    default:
                        System.out.println("Invalid choice. Please select 1, 2, 3, 4, or 5.");
                }
            } catch (InputMismatchException e) {
                System.out.println("Input Error: Please enter a valid number for the amount.");
            } catch (IllegalArgumentException e) {
                System.out.println("Transaction Error: " + e.getMessage());
            } finally {
                // Ensure the scanner buffer is cleared after reading a number
                if (scanner.hasNextLine()) {
                    scanner.nextLine();
                }
            }
        }
        scanner.close();
    }
}