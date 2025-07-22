import os
import aiohttp
import urllib.parse
from services.handle_api_error import handle_api_error
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(1)

async def get_open_orders_api(token, msisdn):
    async with service_rate_limiter:
        service = "open_orders_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}

        base_url = f"{MOLI_BASE_URL}/moli-order/v1/order/open-order"

        params = {"msisdn": msisdn}

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params, headers=headers) as response:
                    response.raise_for_status()
                    payload = await response.json()

                    data = payload if isinstance(payload, dict) else {}
                    # print("🛠️ open_orders_api Payload:", data)
                    
                    extracted_data = {
                        "openOrderFlag": data.get("openOrderFlag", "N/A"),
                        "telco": data.get("telco", "N/A"),
                        "orderNumber": data.get("orderNumber","N/A"),
                        "outletId": data.get("outletId","N/A"),
                        "orderId": data.get("orderId","N/A"),
                        "orderStatus": data.get("ordorderStatuserNumber","N/A"),
                    }

                    if extracted_data["openOrderFlag"] == "N":
                        print(f"🟢 open_orders_api: {response.status} {msisdn} {extracted_data['openOrderFlag']}")
                    elif extracted_data["openOrderFlag"] == "Y":
                        print(f"🟡 open_orders_api: {response.status} {msisdn} {extracted_data['openOrderFlag']} orderNum:{extracted_data['orderNumber']} outletId:{extracted_data['outletId']} orderId:{extracted_data['orderId']} status:{extracted_data['orderStatus']}")
                    else:
                        print(f"🔴 open_orders_api: {response.status} {msisdn} {extracted_data['openOrderFlag']} Unknown order status")

                    result[service_data] = {
                        "customerStatus": f"✅ {response.status}",
                        **extracted_data,
                    }

        except aiohttp.ClientResponseError as error:
            return await handle_api_error(error, msisdn, service)

        except Exception as error:
            return await handle_api_error(error, msisdn, service)
        
        return result