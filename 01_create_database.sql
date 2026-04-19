-- ========================================
-- ATM Transaction Pattern Analysis Project
-- Database and Table Creation Script
-- ========================================

-- Create the database (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS atm_project;

-- Use the database
USE atm_project;

-- Create the transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id VARCHAR(50) UNIQUE NOT NULL,
    atm_location VARCHAR(100) NOT NULL,
    transaction_type ENUM('withdrawal', 'balance_check', 'deposit', 'transfer') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_time DATETIME NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    status ENUM('success', 'failed', 'pending') NOT NULL
);

-- Show table structure
DESCRIBE transactions;
