from pathlib import Path
from dotenv import load_dotenv
import os

#I dont like to retrieve the .env this way T_T
#But I CANNOT SOLVE THE IMPORT ISSUE IN PYTHON without path issue!!!
#Temporary approach until I figure out the better/standard approach. -16Mar2025,Evelyn
#To improve: add python import logging and sys.

def load_env():
    try:
        env_path = Path(__file__).resolve().parent / ".env"
        
        # Check if .env file exists
        if not env_path.exists():
            print(f"❌ Error: .env file not found at {env_path}")
            return False
            
        # Try to load environment variables
        if load_dotenv(env_path):
            # Check required variables
            required_vars = ['AUTH_TOKEN_URL', 'AUTH_CLIENT_ID', 'AUTH_CLIENT_SECRET']
            missing = [var for var in required_vars if not os.getenv(var)]
            
            if not missing:
                print(f"✅ Success: Loaded .env from {env_path}")
                return True
            else:
                print(f"❕ Warning: Missing variables in .env: {', '.join(missing)}")
                return False
        else:
            print(f"❌ Error: Failed to load .env file at {env_path}")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

# Usage in other files
# from config.load_env import load_project_env
# load_project_env()