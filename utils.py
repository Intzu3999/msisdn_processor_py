import asyncio
import aiohttp

async def handle_api_error(error, msisdn):
    """Handles API errors and returns a standardized result."""
    result = {"msisdn": msisdn}
    
    if isinstance(error, aiohttp.ClientResponseError):
        if error.status == 429:
            print(f"🚨 {error.status} Too Many Requests {msisdn}.")
            await asyncio.sleep(5)
            result["getCustomerApiData"] = {"customerStatus": f"❌ {error.status}"}
        else:
            print(f"❌ API Error {error.status} {msisdn}: {error.message}")
            result["getCustomerApiData"] = {"customerStatus": f"❌ {error.status}"}
    
    else:
        print(f"❌ Unknown error {msisdn}: {error}")
        result["getCustomerApiData"] = {"customerStatus": "❌ Unknown Error"}

    return result
