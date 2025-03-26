import os
import time
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

TOKEN_CACHE = {"token": None, "expires_at": 0}
TOKEN_LOCK = asyncio.Lock()  # Prevent concurrent token refresh

async def get_access_token():
    """Fetches a new access token if expired or unavailable, with concurrency safety."""
    global TOKEN_CACHE  

    AUTH_TOKEN_URL = os.getenv("AUTH_TOKEN_URL")
    AUTH_CLIENT_ID = os.getenv("AUTH_CLIENT_ID")
    AUTH_CLIENT_SECRET = os.getenv("AUTH_CLIENT_SECRET")

    if not AUTH_TOKEN_URL or not AUTH_CLIENT_ID or not AUTH_CLIENT_SECRET:
        raise ValueError("❌ Missing required authentication environment variables!")

    current_time = time.time()

    if TOKEN_CACHE["token"] and current_time < TOKEN_CACHE["expires_at"]:
        return TOKEN_CACHE["token"]

    async with TOKEN_LOCK:
        if TOKEN_CACHE["token"] and current_time < TOKEN_CACHE["expires_at"]:
            return TOKEN_CACHE["token"]

        # print("Fetching token...")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    AUTH_TOKEN_URL,
                    data={
                        "grant_type": "client_credentials",
                        "client_id": AUTH_CLIENT_ID,
                        "client_secret": AUTH_CLIENT_SECRET
                    },
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded",
                        "Accept": "*/*"
                    },
                ) as response:
                    response.raise_for_status()
                    data = await response.json()

                    TOKEN_CACHE["token"] = data["access_token"]
                    TOKEN_CACHE["expires_at"] = current_time + data.get("expires_in", 3600) - 10  # 10s buffer

                    print("[OK] Access token")

                    return TOKEN_CACHE["token"]

        except aiohttp.ClientError as e:
            print(f"❌ Network error: {e}")
        except Exception as error:
            print(f"❌ Error fetching access token: {error}")

        raise RuntimeError("❌ Failed to get access token")
