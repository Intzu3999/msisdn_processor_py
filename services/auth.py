import os
import time
import aiohttp
from config.load_env import load_env

load_env()

AUTH_TOKEN_URL = os.getenv("AUTH_TOKEN_URL")
AUTH_CLIENT_ID = os.getenv("AUTH_CLIENT_ID")
AUTH_CLIENT_SECRET = os.getenv("AUTH_CLIENT_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_EXPIRY_TIME = float(os.getenv("ACCESS_TOKEN_EXPIRY_TIME", 0))

async def get_access_token():
    global ACCESS_TOKEN, ACCESS_TOKEN_EXPIRY_TIME  
    
    current_time = time.time()
    if ACCESS_TOKEN and current_time < ACCESS_TOKEN_EXPIRY_TIME:    
        return ACCESS_TOKEN

    try:
        async with aiohttp.ClientSession() as session:
            params = {
                "grant_type": "client_credentials",
                "client_id": AUTH_CLIENT_ID,
                "client_secret": AUTH_CLIENT_SECRET
            }
            
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "*/*"
            }

            async with session.post(
                AUTH_TOKEN_URL,
                params=params,
                headers=headers
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
                ACCESS_TOKEN = data['access_token']
                ACCESS_TOKEN_EXPIRY_TIME = current_time + data['expires_in']
                
                # Update environment variables
                os.environ["ACCESS_TOKEN"] = ACCESS_TOKEN
                os.environ["ACCESS_TOKEN_EXPIRY_TIME"] = str(ACCESS_TOKEN_EXPIRY_TIME)
                
                return ACCESS_TOKEN

    except Exception as error:
        print(f"❌Error fetching access token: {error}")
        raise RuntimeError("❌Failed to get access token")