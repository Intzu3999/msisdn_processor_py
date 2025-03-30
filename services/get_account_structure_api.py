import os
import aiohttp
import pandas as pd
import urllib.parse
from core.handle_api_error import handle_api_error
from services.base_service import BaseService
from services.service_registry import ServiceRegistry
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(5)

class GetAccountStructureAPIService(BaseService):

    async def fetch_data(self, token: str, msisdn: str) -> dict:
        async with service_rate_limiter:
            service = "get_account_structure_api"
            service_data = f"{service}_data"
            level = "customer"
            result = {"msisdn": msisdn}

            api_params = urllib.parse.urlencode({"level": level})
            api_url = f"{MOLI_BASE_URL}/moli-account/v1/accounts/{msisdn}/structure?{api_params}"

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(api_url, headers=headers) as response:
                        response.raise_for_status()
                        payload = await response.json()
                        
                        # print("🛠️ get_account_structure_api Payload:", data)

                        data = payload if isinstance(payload, dict) else {}

                        extracted_data = {
                            "msisdn": data.get("msisdn", "N/A"),
                            "telco": data.get("telco", "N/A"),
                            "productType": data.get("productType", "N/A"),  
                            "productName": data.get("productName", "N/A"), 
                            "startDate": data.get("startDate", "N/A"),
                            "status": data.get("status", "N/A"),
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
    
# Auto-register the service
ServiceRegistry.register("get_account_structure_api", GetAccountStructureAPIService)