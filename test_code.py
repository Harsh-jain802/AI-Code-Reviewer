# This code has a security bug and a logic bug
API_KEY = "12345-ABCDE"  # Hardcoded key

def divide(a, b):
    return a / b  # Bug: Will crash if b is 0
