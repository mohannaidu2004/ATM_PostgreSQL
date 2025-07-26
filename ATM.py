import psycopg2
import datetime

class ATM:
    def __init__(self, conn):
        self.conn = conn
        self.user_id = None
        self.username = None
        self.balance = 0

    def authenticate_user(self, username, pin):
        with self.conn.cursor() as cur:
            cur.execute("SELECT user_id, balance FROM users WHERE username=%s AND pin=%s", (username, pin))
            result = cur.fetchone()
            if result:
                self.user_id, self.balance = result
                self.username = username
                return True
            else:
                return False

    def log_transaction(self, transaction_type, amount):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO atm_transactions (user_id, transaction_type, amount, balance) VALUES (%s, %s, %s, %s)",
                (self.user_id, transaction_type, amount, self.balance)
            )
            self.conn.commit()

    def update_balance(self):
        with self.conn.cursor() as cur:
            cur.execute("UPDATE users SET balance = %s WHERE user_id = %s", (self.balance, self.user_id))
            self.conn.commit()

    def deposit(self, amount):
        self.balance += amount
        self.update_balance()
        self.log_transaction("Deposit", amount)
        print(f"Deposit successful. Current balance: {self.balance}")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance.")
            return
        self.balance -= amount
        self.update_balance()
        self.log_transaction("Withdraw", amount)
        print(f"Withdrawal successful. Remaining balance: {self.balance}")
    def balance_enquiry(self):
        print(f"Current balance: {self.balance}")


conn = psycopg2.connect(
    dbname="testdb",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)

atm = ATM(conn)
username = input("Enter your username: ")
pin = input("Enter your PIN: ")

if atm.authenticate_user(username, pin):
    print(f"Welcome, {username}!")
    while True:
        print("\n1. ATM Menu\n2. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            print("\n1. Deposit\n2. Withdraw\n3. Check Balance")
            choice = input("Choose an option: ")
            if choice == "1":
                amount = float(input("Enter amount to deposit: "))
                atm.deposit(amount)
            elif choice == "2":
                amount = float(input("Enter amount to withdraw: "))
                atm.withdraw(amount)
            elif choice == "3":
                atm.balance_enquiry()
        elif choice == "2":
            print("Thank you! Goodbye.")
            break
        else:
            print("Invalid option. Try again.")
else:
    print("Invalid username or PIN.")

conn.close()
