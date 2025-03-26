import os
import aiohttp
import pandas as pd
import urllib.parse
from utils.handle_api_error import handle_api_error
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(5)

async def get_service_name_api(token, msisdn):
    async with service_rate_limiter:
        service = "get_service_name_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}
        param = "param"

        get_service_name_api_params = urllib.parse.urlencode({param})
        get_service_name_api_url = f"{MOLI_BASE_URL}/moli-account/v1/accounts/{msisdn}/structure?{get_service_name_api_params}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(get_service_name_api_url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    # print("🛠️ get_service_name_api Payload:", data)

                    service_name_data = data if isinstance(data, dict) else {}

                    extracted_data = {
                        "msisdn": service_name_data.get("msisdn", "N/A"),
                    }

                    print(f"✅ get_account_structure_api: {response.status} {msisdn} {extracted_data['telco']} productType:{extracted_data['productType']} {extracted_data['productName']}")

                    result[service_data] = {
                        "customerStatus": f"✅ {response.status}",
                        **extracted_data,
                    }
                    
                    return result

        except aiohttp.ClientResponseError as error:
            return await handle_api_error(error, msisdn, service)

        except Exception as error:
            return await handle_api_error(error, msisdn, service)

        return result