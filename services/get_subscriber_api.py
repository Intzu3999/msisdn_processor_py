import os
import aiohttp
import pandas as pd
import urllib.parse
from services.handle_api_error import handle_api_error
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(1)

async def get_subscriber_api(token, msisdn):
    async with service_rate_limiter:
        service = "get_subscriber_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}
        
        api_params = urllib.parse.urlencode({"msisdn": msisdn})
        api_url = f"{MOLI_BASE_URL}/moli-subscriber/v1/subscriber?{api_params}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=headers) as response:
                    response.raise_for_status()
                    payload = await response.json()

                    # print("🛠️ get_subscriber_api Payload:", data)

                    data = payload if isinstance(payload, dict) else {}

                    extracted_data = {
                        "msisdn": msisdn,  # Ensure `msisdn` is included
                        "telco": data.get("telco", "N/A"),
                        "iccid": data.get("iccid", "N/A"),
                        "payType": data.get("type", "N/A"),
                        "isPrincipal": data.get("isPrincipal", "N/A"),
                        "status": data.get("status", "N/A"),
                        "subscriptionName": next(iter(data.get("subscriptions", {}).get("primary", [{}])), {}).get("name", "N/A"),
                        "customerType": next(iter(data.get("characteristic", {}).get("customerInfo", [{}])), {}).get("type", {}).get("text", "N/A"),
                        "subscriberType": next(iter(data.get("characteristic", {}).get("subscriberInfo", {}).get("subscriberType", [{}])), {}).get("text", "N/A"),
                        "telecomType": next(iter(data.get("characteristic", {}).get("subscriberInfo", {}).get("telecomType", [{}])), {}).get("text", "N/A"),
                        "activeDate": data.get("activeDate", "N/A"),
                        "lifeCycleStatus": data.get("characteristic", {}).get("lifeCycleInfo", {}).get("state", {}).get("status", {}).get("text", "N/A"),
                    }

                    raw_tenure = data.get("characteristic", {}).get("lifeCycleInfo", {}).get("tenure", "0")
                    extracted_data["tenure"] = f"{float(raw_tenure):.2f}" if raw_tenure.replace('.', '', 1).isdigit() else "0.00"

                    print(f"✅ get_subscriber_api: {response.status} {msisdn} {extracted_data['telco']} {extracted_data['payType']} {extracted_data['isPrincipal']} {extracted_data['subscriptionName']} status:{extracted_data['status']} lifecycle:{extracted_data['lifeCycleStatus']}")

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