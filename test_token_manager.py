import asyncio
from services.token_manager import get_token

async def main():
    try:
        token = await get_token()
        print(f"Successfully retrieved token: {token[:10]}...")
    except Exception as e:
        print(f"Failed to initialize: {e}")

if __name__ == "__main__":
    asyncio.run(main())