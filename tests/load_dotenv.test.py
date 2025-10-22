import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve and print environment variables
env_vars = [
    "ACCESS_TOKEN",
    "ACCESS_TOKEN_EXPIRY_TIME",
    "AUTH_TOKEN_URL",
    "AUTH_CLIENT_ID",
    "AUTH_CLIENT_SECRET",
    "ACCOUNT_BASE_URL",
    "MOLI_BASE_URL",
    "EMAIL_USER",
    "EMAIL_PASSWORD",
    "EMAIL_TO",
    "SMTP_SERVER",
    "SMTP_PORT"
]

all_passed = True

for var in env_vars:
    if os.getenv(var):
        print(f"✅ {var}: PASSED")
    else:
        print(f"❌ {var}: FAILED")
        all_passed = False