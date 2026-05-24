import os
import sqlite3

#  ISSUE 1: Security Risk - Hardcoded Sensitive Data
# In a real app, this should be in an environment variable.
ADMIN_PASSWORD = "super-secret-password-123"
API_KEY = "gsk_y9823hfoiwehf9823hfoihwef" 

def get_user_balance(user_id):
    #  ISSUE 2: Security Risk - SQL Injection
    # Using string formatting for queries is dangerous.
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT balance FROM accounts WHERE id = '{user_id}'"
    cursor.execute(query)
    return cursor.fetchone()

def calculate_discount(price, discount_percent):
    #  ISSUE 3: Logic Bug - Potential Division by Zero
    # If discount_percent is 100, this might cause issues depending on logic,
    # but more importantly, if we divided by (100 - discount_percent):
    return price / (100 - discount_percent)

def process_data(items):
    #  ISSUE 4: Performance/Code Smell - Unused Variable & Poor Naming
    temp_val = 100 # Unused
    for i in range(len(items)):
        # Doing something slow in a loop
        print("Processing item...")
    return True
