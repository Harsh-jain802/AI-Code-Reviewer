def connect_db():
    # SECURITY BUG: Hardcoded credentials
    user = "admin"
    password = "password123"
    print(f"Connecting as {user}...")

def risky_math(n):
    # LOGIC BUG: Division by zero if n is 10
    return 100 / (n - 10)
