import os
import aiohttp
import urllib.parse
from utils.handle_api_error import handle_api_error
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(1)

async def get_customer_api(token, msisdn):
    async with service_rate_limiter:
        service = "get_customer_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}

        api_params = urllib.parse.urlencode({"msisdn": msisdn})
        api_url = f"{MOLI_BASE_URL}/moli-customer/v3/customer?{api_params}"

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    response.raise_for_status()
                    payload = await response.json()

                    # print("🛠️ get_customer_api Payload:", data)

                    data = payload[0] if isinstance(payload, list) and payload else {}

                    personal_info = data.get("personalInfo", [{}])[0]
                    identification = personal_info.get("identification", [{}])[0]
                    contact_info = data.get("contact", {})
                    address = contact_info.get("address", [{}])[0]

                    extracted_data = {
                        "idNo": identification.get("idNo", "N/A"),
                        "idType": identification.get("type", {}).get("code", "NA"),
                        "countryCode": address.get("country", {}).get("code", "NA"),
                    }

                    print(f"✅ get_customer_api: {response.status} {msisdn} id:{extracted_data['idType']} {extracted_data['idNo']} countryCode:{extracted_data['countryCode']}")

                    result[service_data] = {
                        "customerStatus": f"✅ {response.status}",
                        **extracted_data,  # Expands dictionary to maintain consistency
                    }

        except aiohttp.ClientResponseError as error:
            return await handle_api_error(error, msisdn, service)

        except Exception as error:
            return await handle_api_error(error, msisdn, service)
        
        return result