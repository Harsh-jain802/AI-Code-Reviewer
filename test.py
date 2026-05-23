def check_password(input):
    # SECURITY BUG: Hardcoded password
    if input == "admin123":
        return True

def divide(a, b):
    # LOGIC BUG: Will crash if b is 0
    return a / b

# CODE SMELL: Unused variable
x = 100
