import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Root directory
load_dotenv()

# Function to get environment variables
def get_env(var_name, default=None):
    return os.getenv(var_name, default)

DB_CONFIG = {
    "host": "localhost",
    "user": "",
    "password": "",
    "database": "api_data",
}

# API Config
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_EXPIRY_TIME = os.getenv("ACCESS_TOKEN_EXPIRY_TIME")
AUTH_TOKEN_URL = os.getenv("AUTH_TOKEN_URL")
AUTH_CLIENT_ID = os.getenv("AUTH_CLIENT_ID")
AUTH_CLIENT_SECRET = os.getenv("AUTH_CLIENT_SECRET")
ACCOUNT_BASE_URL = os.getenv("ACCOUNT_BASE_URL")
MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

# Paths (Example: Playwright, Selenium, Android Emulator)
SELENIUM_DRIVER_PATH = os.path.join(BASE_DIR, "drivers", "chromedriver.exe")
PLAYWRIGHT_BINARY_PATH = os.path.join(BASE_DIR, "browsers", "playwright.exe")
ANDROID_EMULATOR_PATH = "C:/Users/YourUser/AppData/Local/Android/sdk/emulator/emulator.exe"

# Email Config
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO", "intzucareers@gmail.com")

# GMAIL
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))

# OUTLOOK
# SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.office365.com")
# SMTP_PORT = int(os.getenv("SMTP_PORT", 587))