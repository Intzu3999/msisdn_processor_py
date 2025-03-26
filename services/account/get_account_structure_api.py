import os
import aiohttp
import pandas as pd
import urllib.parse
from utils.handle_api_error import handle_api_error
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(5)

async def get_account_structure_api(token, msisdn):
    async with service_rate_limiter:
        service = "get_account_structure_api"
        service_data = f"{service}_data"
        level = "customer"
        result = {"msisdn": msisdn}

        get_account_structure_api_params = urllib.parse.urlencode({"level": level})
        get_account_structure_api_url = f"{MOLI_BASE_URL}/moli-account/v1/accounts/{msisdn}/structure?{get_account_structure_api_params}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(get_account_structure_api_url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()
                    
                    # print("🛠️ get_account_structure_api Payload:", data)

                    account_structure_data = data if isinstance(data, dict) else {}

                    extracted_data = {
                        "msisdn": account_structure_data.get("msisdn", "N/A"),
                        "telco": account_structure_data.get("telco", "N/A"),
                        "productType": account_structure_data.get("productType", "N/A"),  
                        "productName": account_structure_data.get("productName", "N/A"), 
                        "startDate": account_structure_data.get("startDate", "N/A"),
                        "status": account_structure_data.get("status", "N/A"),
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