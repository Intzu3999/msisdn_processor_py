import os
import aiohttp
import urllib.parse
from utils.handle_api_error import handle_api_error
from asyncio import Semaphore
from services.auth import get_access_token

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(1)

async def get_customer_api(msisdn):
    async with service_rate_limiter:
        service = "get_customer_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}
        try:
            token = await get_access_token()
        except Exception as error:
            print(f"❌ Failed to fetch token: {error}")
            return result  # Return empty result

        get_customer_api_params = urllib.parse.urlencode({"msisdn": msisdn})
        get_customer_api_url = f"{MOLI_BASE_URL}/moli-customer/v3/customer?{get_customer_api_params}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    get_customer_api_url,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    },
                ) as response:

                    response.raise_for_status()
                    data = await response.json()

                    # print("🛠️ get_customer_api Payload:", data)

                    customer_data = data[0] if isinstance(data, list) and data else {}

                    personal_info = customer_data.get("personalInfo", [{}])[0]
                    identification = personal_info.get("identification", [{}])[0]
                    contact_info = customer_data.get("contact", {})
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