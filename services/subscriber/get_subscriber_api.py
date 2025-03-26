import os
import aiohttp
import pandas as pd
import urllib.parse
from utils.handle_api_error import handle_api_error
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(5)

async def get_subscriber_api(token, msisdn):
    async with service_rate_limiter:
        service = "get_subscriber_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}
        
        get_subscriber_api_params = urllib.parse.urlencode({"msisdn": msisdn})
        get_subscriber_api_url = f"{MOLI_BASE_URL}/moli-subscriber/v1/subscriber?{get_subscriber_api_params}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(get_subscriber_api_url, headers=headers) as response:
                    response.raise_for_status()
                    data = await response.json()

                    # print("🛠️ get_subscriber_api Payload:", data)

                    subscriber_data = data if isinstance(data, dict) else {}

                    extracted_data = {
                        "msisdn": msisdn,  # Ensure `msisdn` is included
                        "telco": subscriber_data.get("telco", "N/A"),
                        "payType": subscriber_data.get("type", "N/A"),
                        "isPrincipal": subscriber_data.get("isPrincipal", "N/A"),
                        "status": subscriber_data.get("status", "N/A"),
                        "subscriptionName": next(iter(subscriber_data.get("subscriptions", {}).get("primary", [{}])), {}).get("name", "N/A"),
                        "customerType": next(iter(subscriber_data.get("characteristic", {}).get("customerInfo", [{}])), {}).get("type", {}).get("text", "N/A"),
                        "subscriberType": next(iter(subscriber_data.get("characteristic", {}).get("subscriberInfo", {}).get("subscriberType", [{}])), {}).get("text", "N/A"),
                        "telecomType": next(iter(subscriber_data.get("characteristic", {}).get("subscriberInfo", {}).get("telecomType", [{}])), {}).get("text", "N/A"),
                        "activeDate": subscriber_data.get("activeDate", "N/A"),
                    }

                    raw_tenure = subscriber_data.get("characteristic", {}).get("lifeCycleInfo", {}).get("tenure", "0")
                    extracted_data["tenure"] = f"{float(raw_tenure):.2f}" if raw_tenure.replace('.', '', 1).isdigit() else "0.00"

                    print(f"✅ get_subscriber_api: {response.status} {msisdn} {extracted_data['telco']} {extracted_data['payType']} {extracted_data['isPrincipal']} {extracted_data['status']} tenure:{extracted_data['tenure']}")

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