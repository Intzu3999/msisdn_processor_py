import time
from .auth import get_access_token

cached_token = None
token_expiry = 0

async def get_token():
    global cached_token, token_expiry
    
    if cached_token and time.time() < token_expiry:
        return cached_token

    try:
        token = await get_access_token()
        cached_token = token
        token_expiry = time.time() + 3600  # 1 hour expiration
        return token
        
    except Exception as error:
        print(f"❌ Failed to fetch token: {error}")
        raise