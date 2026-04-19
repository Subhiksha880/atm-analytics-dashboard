-- Add more sample transactions to make the dashboard more interesting
USE atm_project;

INSERT INTO transactions (transaction_id, atm_location, transaction_type, amount, transaction_time, customer_id, status) VALUES
-- More Downtown Branch transactions
('TXN006', 'Downtown Branch', 'withdrawal', 300.00, '2024-01-15 14:30:00', 'CUST006', 'success'),
('TXN007', 'Downtown Branch', 'deposit', 800.00, '2024-01-15 15:45:00', 'CUST007', 'success'),
('TXN008', 'Downtown Branch', 'transfer', 150.00, '2024-01-15 16:20:00', 'CUST008', 'success'),
('TXN009', 'Downtown Branch', 'balance_check', 0.00, '2024-01-15 17:00:00', 'CUST009', 'success'),
('TXN010', 'Downtown Branch', 'withdrawal', 450.00, '2024-01-15 18:15:00', 'CUST010', 'success'),

-- More Airport Terminal transactions
('TXN011', 'Airport Terminal', 'withdrawal', 750.00, '2024-01-15 19:30:00', 'CUST011', 'success'),
('TXN012', 'Airport Terminal', 'deposit', 1200.00, '2024-01-15 20:45:00', 'CUST012', 'success'),
('TXN013', 'Airport Terminal', 'transfer', 300.00, '2024-01-15 21:20:00', 'CUST013', 'success'),
('TXN014', 'Airport Terminal', 'balance_check', 0.00, '2024-01-15 22:00:00', 'CUST014', 'success'),
('TXN015', 'Airport Terminal', 'withdrawal', 950.00, '2024-01-15 23:15:00', 'CUST015', 'failed'),

-- More Shopping Mall transactions
('TXN016', 'Shopping Mall', 'withdrawal', 180.00, '2024-01-15 10:30:00', 'CUST016', 'success'),
('TXN017', 'Shopping Mall', 'deposit', 600.00, '2024-01-15 11:45:00', 'CUST017', 'success'),
('TXN018', 'Shopping Mall', 'transfer', 120.00, '2024-01-15 12:20:00', 'CUST018', 'success'),
('TXN019', 'Shopping Mall', 'balance_check', 0.00, '2024-01-15 13:00:00', 'CUST019', 'success'),
('TXN020', 'Shopping Mall', 'withdrawal', 220.00, '2024-01-15 14:15:00', 'CUST020', 'success'),

-- More University Campus transactions
('TXN021', 'University Campus', 'withdrawal', 80.00, '2024-01-15 08:30:00', 'CUST021', 'success'),
('TXN022', 'University Campus', 'deposit', 200.00, '2024-01-15 09:45:00', 'CUST022', 'success'),
('TXN023', 'University Campus', 'transfer', 60.00, '2024-01-15 10:20:00', 'CUST023', 'success'),
('TXN024', 'University Campus', 'balance_check', 0.00, '2024-01-15 11:00:00', 'CUST024', 'success'),
('TXN025', 'University Campus', 'withdrawal', 95.00, '2024-01-15 12:15:00', 'CUST025', 'success'),

-- Hospital Complex transactions
('TXN026', 'Hospital Complex', 'withdrawal', 350.00, '2024-01-15 07:30:00', 'CUST026', 'success'),
('TXN027', 'Hospital Complex', 'deposit', 900.00, '2024-01-15 08:45:00', 'CUST027', 'success'),
('TXN028', 'Hospital Complex', 'transfer', 200.00, '2024-01-15 09:20:00', 'CUST028', 'success'),
('TXN029', 'Hospital Complex', 'balance_check', 0.00, '2024-01-15 10:00:00', 'CUST029', 'success'),
('TXN030', 'Hospital Complex', 'withdrawal', 420.00, '2024-01-15 11:15:00', 'CUST030', 'success');

-- Verify the new data
SELECT COUNT(*) as total_transactions FROM transactions;
SELECT atm_location, COUNT(*) as count FROM transactions GROUP BY atm_location ORDER BY count DESC;
