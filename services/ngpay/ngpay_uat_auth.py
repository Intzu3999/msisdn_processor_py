import os
import time
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

NGPAY_TOKEN_CACHE = {"token": None, "expires_at": 0}
NGPAY_TOKEN_LOCK = asyncio.Lock()

async def ngpay_uat_auth():
    """Fetches and caches NGPAY login token with concurrency safety."""
    global NGPAY_TOKEN_CACHE

    NGPAY_DEV_BASE_URL = os.getenv("NGPAY_DEV_BASE_URL")
    NGPAY_CLIENT_EMAIL = os.getenv("NGPAY_CLIENT_EMAIL")
    NGPAY_CLIENT_PASSWORD = os.getenv("NGPAY_CLIENT_PASSWORD")
    XSRF_TOKEN = os.getenv("XSRF-TOKEN")

    if not all([NGPAY_DEV_BASE_URL, NGPAY_CLIENT_EMAIL, NGPAY_CLIENT_PASSWORD,XSRF_TOKEN]):
        raise ValueError("❌ Missing NGPAY environment variables")

    current_time = time.time()

    # Return cached token if still valid
    if NGPAY_TOKEN_CACHE["token"] and current_time < NGPAY_TOKEN_CACHE["expires_at"]:
        return NGPAY_TOKEN_CACHE["token"]

    async with NGPAY_TOKEN_LOCK:
        # Double-check cache after acquiring lock
        if NGPAY_TOKEN_CACHE["token"] and current_time < NGPAY_TOKEN_CACHE["expires_at"]:
            return NGPAY_TOKEN_CACHE["token"]

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{NGPAY_DEV_BASE_URL}/online-store-api/v1/login",
                    json={
                        "client_email": NGPAY_CLIENT_EMAIL,
                        "client_password": NGPAY_CLIENT_PASSWORD,
                    },
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "PostmanRuntime/7.43.3",                        
                        "XSRF-TOKEN": XSRF_TOKEN
                    }
                ) as response:
                    response.raise_for_status()
                    data = await response.json()

                    token = data.get("token")
                    if not token:
                        raise ValueError("❌ Token not found in response")

                    # Cache token with 1 hour expiry (adjust as needed)
                    NGPAY_TOKEN_CACHE["token"] = token
                    NGPAY_TOKEN_CACHE["expires_at"] = current_time + 3600 - 10  # 10s buffer

                    # Optional: Set environment variable (for current process)
                    os.environ["NGPAY_ACCESS_TOKEN"] = token

                    return token

        except aiohttp.ClientResponseError as e:
            print(f"❌ API Error ({e.status}): {e.message}")
        except aiohttp.ClientError as e:
            print(f"❌ Network error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

        raise RuntimeError("❌ Failed to get NGPAY access token")
try:
    asyncio.run(ngpay_uat_auth())
except Exception as e:
    print("Fatal error:", e)