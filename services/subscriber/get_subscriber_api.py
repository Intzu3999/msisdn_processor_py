import os
import aiohttp
import pandas as pd
import urllib.parse
from utils.handle_api_error import handle_api_error
from asyncio import Semaphore
from services.auth import get_access_token

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(5)

async def get_subscriber_api(msisdn):
    async with service_rate_limiter:
        service = "get_subscriber_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}
        try:
            token = await get_access_token()
        except Exception as error:
            print(f"❌ Failed to fetch token: {error}")
            return result  # Return empty result
        
        get_subscriber_api_params = urllib.parse.urlencode({"msisdn": msisdn})
        get_subscriber_api_url = f"{MOLI_BASE_URL}/moli-subscriber/v1/subscriber?{get_subscriber_api_params}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    get_subscriber_api_url,
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json",
                    },
                ) as response:

                    response.raise_for_status()
                    data = await response.json()

                    # print("🛠️ get_subscriber_api Payload:", data)

                    subscriber_telco = data.get("telco", "Null")
                    active_date = data.get("activeDate", "Null")
                    pay_type = data.get("type", "Null")
                    is_principal = data.get("isPrincipal", "Null")
                    status = data.get("status", "Null")
                    subscription_name = data.get("subscriptions", {}).get("primary", [{}])[0].get("name", "N/A")

                    characteristic = data.get("characteristic", {})
                    customer_type = characteristic.get("customerInfo", [{}])[0].get("type", {}).get("text", "Null")
                    subscriber_type = characteristic.get("subscriberInfo", {}).get("subscriberType", [{}])[0].get("text", "Null")
                    telecom_type = characteristic.get("subscriberInfo", {}).get("telecomType", [{}])[0].get("text", "Null")
                    raw_tenure = characteristic.get("lifeCycleInfo", {}).get("tenure", "0")

                    tenure = f"{float(raw_tenure):.2f}" if raw_tenure.replace('.', '', 1).isdigit() else "0.00"

                    print(f"✅ get_subscriber_api: {response.status} {subscriber_telco} {pay_type} isPrincipal:{is_principal} {status} tenure:{tenure}")

                    result[service_data] = {
                        "httpStatus": f"✅ {response.status}",
                        "telco": subscriber_telco,
                        "activeDate": active_date,
                        "payType": pay_type,
                        "isPrincipal": is_principal,
                        "status": status,
                        "subscriptionName": subscription_name,
                        "customerType": customer_type,
                        "subscriberType": subscriber_type,
                        "telecomType": telecom_type,
                        "tenure": tenure,
                    }

        except aiohttp.ClientResponseError as error:
            return await handle_api_error(error, msisdn, service)

        except Exception as error:
            return await handle_api_error(error, msisdn, service)
        
        return result