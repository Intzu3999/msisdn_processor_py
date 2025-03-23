import asyncio
import aiohttp

async def handle_api_error(error, msisdn, service):
    """Handles API errors and returns a standardized result."""
    result = {"msisdn": msisdn}
    
    service_data = f"{service}_data"
    result[service_data] = {}
    
    if isinstance(error, aiohttp.ClientResponseError):
        if error.status == 429:
            print(f"🚨 {service} {error.status} Too Many Requests {msisdn}")
            await asyncio.sleep(5)
            result[service_data]["customerStatus"] = f"❌ {error.status}"
        else:
            print(f"❌ {service} {error.status} Error in API {msisdn} - {error.message}")
            result[service_data]["customerStatus"] = f"❌ {error.status}"
    
    else:
        print(f"❌ {service} Unknown error {msisdn} - {error}")
        result[service_data]["customerStatus"] = f"❌ {error.status}"

    return result
