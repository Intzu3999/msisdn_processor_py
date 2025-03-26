import os
import aiohttp
import urllib.parse
from utils.handle_api_error import handle_api_error
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(5)

async def get_contract_api(token, msisdn):
    async with service_rate_limiter:
        service = "get_contract_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}

        api_url = f"{MOLI_BASE_URL}/moli-customer/v1/customer/{msisdn}/contract"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    response.raise_for_status()
                    payload = await response.json()

                    # print("🛠️ get_contract_api Payload:", data)

                    data = payload if isinstance(payload, dict) else {}

                    extracted_data = {
                        "msisdn": data.get("msisdn", "N/A"),
                        "telco": data.get("telco", "N/A"),
                        "productType": data.get("productType", "N/A"),  
                        "productName": data.get("productName", "N/A"), 
                        "startDate": data.get("startDate", "N/A"),
                        "status": data.get("status", "N/A"),
                    }

                    print(f"✅ get_contract_api: {response.status} {msisdn} {extracted_data['telco']} productType:{extracted_data['productType']} {extracted_data['productName']}")

                    result[service_data] = {
                        "customerStatus": f"✅ {response.status}",
                        **extracted_data,
                    }

        except aiohttp.ClientResponseError as error:
            return await handle_api_error(error, msisdn, service)

        except Exception as error:
            return await handle_api_error(error, msisdn, service)

        return result