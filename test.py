import os

# BUG: This is a security risk (hardcoded secret)
API_KEY = "sk-1234567890abcdef" 

def calculate_area(radius):
    # BUG: No error handling for negative numbers
    return 3.14 * radius * radius

def login(user, password):
    # BUG: Plain text password comparison
    if password == "admin123":
        return True
