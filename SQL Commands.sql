/* Creating the table to store users Data*/
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    pin TEXT NOT NULL,
    balance REAL DEFAULT 0
);

/* Creating the table to store atm_transaction Data*/
CREATE TABLE atm_transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_type TEXT,
    amount REAL,
    balance REAL
);
	
/* Command to insert the user details into the table*/

INSERT INTO users (username, pin, balance) VALUES ('mohan', '1234', 0);

/* Displaying the user and transaction Details*/

SELECT * FROM users
SELECT * FROM atm_transactions
