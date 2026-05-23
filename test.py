import os

# BUG 1: Hardcoded sensitive information
API_KEY = "gsk_5566778899aabbccddeeff" 

def divide_numbers(a, b):
    # BUG 2: Potential division by zero error
    return a / b

def save_user(username, password):
    # BUG 3: Storing password in plain text
    print(f"Saving user {username} with password {password}")
# Testing the new UI
