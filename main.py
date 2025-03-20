import asyncio
from services.auth import get_access_token

async def main():
    token = await get_access_token()
    print(f"🔑 Your access token: {token}")

asyncio.run(main())