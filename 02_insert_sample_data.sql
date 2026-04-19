-- ========================================
-- ATM Transaction Pattern Analysis Project
-- Sample Data Insertion Script
-- ========================================

USE atm_project;

-- Clear existing data (for fresh start)
TRUNCATE TABLE transactions;

-- Insert sample ATM transaction data
INSERT INTO transactions (transaction_id, atm_location, transaction_type, amount, transaction_time, customer_id, status) VALUES
-- Downtown Branch transactions
('TXN001', 'Downtown Branch', 'withdrawal', 500.00, '2024-01-15 08:30:00', 'CUST001', 'success'),
('TXN002', 'Downtown Branch', 'balance_check', 0.00, '2024-01-15 09:15:00', 'CUST002', 'success'),
('TXN003', 'Downtown Branch', 'withdrawal', 200.00, '2024-01-15 10:45:00', 'CUST003', 'success'),
('TXN004', 'Downtown Branch', 'deposit', 1000.00, '2024-01-15 11:30:00', 'CUST004', 'success'),
('TXN005', 'Downtown Branch', 'withdrawal', 150.00, '2024-01-15 12:00:00', 'CUST005', 'success'),
('TXN006', 'Downtown Branch', 'transfer', 300.00, '2024-01-15 13:30:00', 'CUST006', 'success'),
('TXN007', 'Downtown Branch', 'withdrawal', 400.00, '2024-01-15 14:15:00', 'CUST007', 'success'),
('TXN008', 'Downtown Branch', 'balance_check', 0.00, '2024-01-15 15:00:00', 'CUST008', 'success'),
('TXN009', 'Downtown Branch', 'withdrawal', 250.00, '2024-01-15 16:30:00', 'CUST009', 'success'),
('TXN010', 'Downtown Branch', 'withdrawal', 600.00, '2024-01-15 17:45:00', 'CUST010', 'success'),

-- Airport Terminal transactions
('TXN011', 'Airport Terminal', 'withdrawal', 1000.00, '2024-01-15 06:00:00', 'CUST011', 'success'),
('TXN012', 'Airport Terminal', 'balance_check', 0.00, '2024-01-15 07:30:00', 'CUST012', 'success'),
('TXN013', 'Airport Terminal', 'withdrawal', 750.00, '2024-01-15 08:15:00', 'CUST013', 'success'),
('TXN014', 'Airport Terminal', 'withdrawal', 300.00, '2024-01-15 09:45:00', 'CUST014', 'success'),
('TXN015', 'Airport Terminal', 'deposit', 2000.00, '2024-01-15 10:30:00', 'CUST015', 'success'),
('TXN016', 'Airport Terminal', 'withdrawal', 500.00, '2024-01-15 11:15:00', 'CUST016', 'success'),
('TXN017', 'Airport Terminal', 'transfer', 800.00, '2024-01-15 12:30:00', 'CUST017', 'success'),
('TXN018', 'Airport Terminal', 'withdrawal', 450.00, '2024-01-15 13:45:00', 'CUST018', 'success'),
('TXN019', 'Airport Terminal', 'balance_check', 0.00, '2024-01-15 14:30:00', 'CUST019', 'success'),
('TXN020', 'Airport Terminal', 'withdrawal', 900.00, '2024-01-15 15:15:00', 'CUST020', 'success'),

-- Shopping Mall transactions
('TXN021', 'Shopping Mall', 'withdrawal', 200.00, '2024-01-15 10:00:00', 'CUST021', 'success'),
('TXN022', 'Shopping Mall', 'balance_check', 0.00, '2024-01-15 11:30:00', 'CUST022', 'success'),
('TXN023', 'Shopping Mall', 'withdrawal', 150.00, '2024-01-15 12:45:00', 'CUST023', 'success'),
('TXN024', 'Shopping Mall', 'deposit', 500.00, '2024-01-15 13:30:00', 'CUST024', 'success'),
('TXN025', 'Shopping Mall', 'withdrawal', 300.00, '2024-01-15 14:15:00', 'CUST025', 'success'),
('TXN026', 'Shopping Mall', 'transfer', 200.00, '2024-01-15 15:30:00', 'CUST026', 'success'),
('TXN027', 'Shopping Mall', 'withdrawal', 100.00, '2024-01-15 16:45:00', 'CUST027', 'success'),
('TXN028', 'Shopping Mall', 'balance_check', 0.00, '2024-01-15 17:30:00', 'CUST028', 'success'),
('TXN029', 'Shopping Mall', 'withdrawal', 250.00, '2024-01-15 18:15:00', 'CUST029', 'success'),
('TXN030', 'Shopping Mall', 'withdrawal', 180.00, '2024-01-15 19:00:00', 'CUST030', 'success'),

-- University Campus transactions
('TXN031', 'University Campus', 'withdrawal', 50.00, '2024-01-15 07:00:00', 'CUST031', 'success'),
('TXN032', 'University Campus', 'balance_check', 0.00, '2024-01-15 08:30:00', 'CUST032', 'success'),
('TXN033', 'University Campus', 'withdrawal', 80.00, '2024-01-15 09:15:00', 'CUST033', 'success'),
('TXN034', 'University Campus', 'withdrawal', 120.00, '2024-01-15 10:30:00', 'CUST034', 'success'),
('TXN035', 'University Campus', 'deposit', 300.00, '2024-01-15 11:45:00', 'CUST035', 'success'),
('TXN036', 'University Campus', 'withdrawal', 60.00, '2024-01-15 12:30:00', 'CUST036', 'success'),
('TXN037', 'University Campus', 'transfer', 150.00, '2024-01-15 13:15:00', 'CUST037', 'success'),
('TXN038', 'University Campus', 'withdrawal', 90.00, '2024-01-15 14:30:00', 'CUST038', 'success'),
('TXN039', 'University Campus', 'balance_check', 0.00, '2024-01-15 15:45:00', 'CUST039', 'success'),
('TXN040', 'University Campus', 'withdrawal', 110.00, '2024-01-15 16:30:00', 'CUST040', 'success'),

-- Hospital Complex transactions
('TXN041', 'Hospital Complex', 'withdrawal', 300.00, '2024-01-15 06:30:00', 'CUST041', 'success'),
('TXN042', 'Hospital Complex', 'balance_check', 0.00, '2024-01-15 07:45:00', 'CUST042', 'success'),
('TXN043', 'Hospital Complex', 'withdrawal', 400.00, '2024-01-15 08:30:00', 'CUST043', 'success'),
('TXN044', 'Hospital Complex', 'deposit', 800.00, '2024-01-15 09:15:00', 'CUST044', 'success'),
('TXN045', 'Hospital Complex', 'withdrawal', 250.00, '2024-01-15 10:30:00', 'CUST045', 'success'),
('TXN046', 'Hospital Complex', 'transfer', 500.00, '2024-01-15 11:45:00', 'CUST046', 'success'),
('TXN047', 'Hospital Complex', 'withdrawal', 350.00, '2024-01-15 12:30:00', 'CUST047', 'success'),
('TXN048', 'Hospital Complex', 'balance_check', 0.00, '2024-01-15 13:15:00', 'CUST048', 'success'),
('TXN049', 'Hospital Complex', 'withdrawal', 450.00, '2024-01-15 14:45:00', 'CUST049', 'success'),
('TXN050', 'Hospital Complex', 'withdrawal', 200.00, '2024-01-15 15:30:00', 'CUST050', 'success'),

-- Additional transactions for different times
('TXN051', 'Downtown Branch', 'withdrawal', 800.00, '2024-01-15 20:00:00', 'CUST051', 'success'),
('TXN052', 'Airport Terminal', 'withdrawal', 1200.00, '2024-01-15 21:30:00', 'CUST052', 'success'),
('TXN053', 'Shopping Mall', 'withdrawal', 300.00, '2024-01-15 19:30:00', 'CUST053', 'success'),
('TXN054', 'University Campus', 'withdrawal', 70.00, '2024-01-15 18:00:00', 'CUST054', 'success'),
('TXN055', 'Hospital Complex', 'withdrawal', 500.00, '2024-01-15 17:00:00', 'CUST055', 'success');

-- Verify data insertion
SELECT COUNT(*) as total_records FROM transactions;
SELECT * FROM transactions LIMIT 5;
