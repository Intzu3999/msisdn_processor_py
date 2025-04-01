import os
import time
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

class NgPayDevAuth:
    _token_cache = {"token": None, "expires_at": 0}
    _lock = asyncio.Lock()
    
    @classmethod
    async def login(cls):
        """Authenticate using email/password and return a token."""
        client_email = os.getenv("client_email")
        client_password = os.getenv("client_password")
        base_url = os.getenv("base_url")
        token = os.getenv("token")
        XSRF_TOKEN = os.getenv("XSRF-TOKEN")

        if not all([client_email, client_password, base_url, token, XSRF_TOKEN]):
            raise ValueError("Missing required environment variables")
            
        # Return cached token if valid
        if cls._is_token_valid():
            return cls._token_cache["token"]
            
        async with cls._lock:
            # Double-check after acquiring lock
            if cls._is_token_valid():
                return cls._token_cache["token"]
                
            token = await cls._request_new_token(base_url, client_email, client_password, token, XSRF_TOKEN)
            cls._update_token_cache(token)
            return token
    
    @classmethod
    def _is_token_valid(cls):
        """Check if cached token is still valid."""
        return (
            cls._token_cache["token"] and 
            time.time() < cls._token_cache["expires_at"]
        )
    
    @classmethod
    async def _request_new_token(cls, base_url, client_email, client_password,token, XSRF_TOKEN):
        """Make API request to get new token."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{base_url}/online-store-api/v1/login",
                    json={"email": client_email, "password": client_password},
                    headers={
                        'Authorization': 'Bearer {token}',
                        "Content-Type": "application/json",
                        "User-Agent": "PostmanRuntime/7.43.3",
                        # "sec-fetch-site": "none",
                        # "accept-encoding": "gzip, deflate, br, zstd",
                        # "sec-fetch-site": "none",
                        # "secret": "ngpay",
                        # "x-amz-cf-id": "QZesJoNtrqqh_KeIEPQoVIoA6UvMTZyHOWZlNhAc5Ke0BJ0ww7IlpQ==",
                        # "cookie": "XSRF-TOKEN=eyJpdiI6ImN4ejAyWE1qVkVPZTN0bXl0WjFTMHc9PSIsInZhbHVlIjoiOFE0TjIwOVRQOVV6elk3N20rNGg0MWdJa3dzMGd5SDU3SmZ6ZzJER2t1bkhhQU5xalFmY2djZG9paGszNmVCTW1OTVhmdURDSS94NnNXZjk4VGwwTkpUOGFFcHNsSHJKZ0tGbEZoRm9rNXU2Sk5IZ1VrQy9XZHdlaGx0SldwZFYiLCJtYWMiOiIzZGQ0MDQ0OGU3MjUzMjdhMWMzNDVkZjE2ZDIyMjc0MmYwY2FiOTlmOTFjZTY2NTk5NzhkZDliYzZmNjIyNTI5IiwidGFnIjoiIn0%3D; uat_ngpay_dashboard_session=eyJpdiI6ImN1WGozNVZvY1NRNUJBQnBYYUtiM1E9PSIsInZhbHVlIjoiNENTT2FFZ3V3dTBjWmNaMGk4MmY1SE8zakpEbG1zcFRpMVB4cmZjbTNwWG9SQkVjWlRPdmR3RnBBaDZGYkxGeGF1MWhzSUV5cEM2aThNdDhxNGdtekRpQXVRTDVYa3U2SFVGZVdXZ3RZMjVkVllWWU01TGwzcmxoNlYxSmlxQVQiLCJtYWMiOiJiN2I5MzhkYWQyZDE2ZDA5Mzc5OTU4YTJhNjJhM2M5MTA1ZjEzNDIxOTkxMWM1ZWY1OTIyOTZjYzExMGY5N2MwIiwidGFnIjoiIn0%3D",
                        # "VIA": "3.0 6a98c19531a35c06dca95806ad705bd0.cloudfront.net (CloudFront)",
                        # "host": "dkxfwptp2ybrw.cloudfront.net",
                        # "x-forwarded-port": "80",
                        # "x-forwarded-for": "51.158.175.218, 18.68.55.47",
                        # "XSRF-TOKEN": XSRF_TOKEN
                    }
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    if not (token := data.get("token")):
                        raise ValueError("Token not found in response")
                        
                    return token
                    
        except aiohttp.ClientResponseError as e:
            print(f"API Error {e.status}: {e.message}")
            raise
        except aiohttp.ClientError as e:
            print(f"Network Error: {str(e)}")
            raise
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            raise
    
    @classmethod
    def _update_token_cache(cls, token, expires_in=3600):
        """Update token cache with new token."""
        cls._token_cache = {
            "token": token,
            "expires_at": time.time() + expires_in - 10  # 10s buffer
        }
        os.environ["NGPAY_ACCESS_TOKEN"] = token  # Optional env var update


async def main():
    try:
        token = await NgPayDevAuth.login()
        print(f"Login successful. Token: {token[:15]}...")
    except Exception as e:
        print(f"Login failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())