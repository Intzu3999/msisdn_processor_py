import os
from dotenv import load_dotenv

# config.py is the import ../../../ of the JavaScript
# this is the best practice in python to manage the imports of directories

# Load .env from the project root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Root directory
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

# Function to get environment variables
def get_env(var_name, default=None):
    return os.getenv(var_name, default)

    
# Paths (Example: Playwright, Selenium, Android Emulator)
SELENIUM_DRIVER_PATH = os.path.join(BASE_DIR, "drivers", "chromedriver.exe")
PLAYWRIGHT_BINARY_PATH = os.path.join(BASE_DIR, "browsers", "playwright.exe")
ANDROID_EMULATOR_PATH = "C:/Users/YourUser/AppData/Local/Android/sdk/emulator/emulator.exe"
