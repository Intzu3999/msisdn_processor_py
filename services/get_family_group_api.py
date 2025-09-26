import os
import aiohttp
import pandas as pd
import urllib.parse
from services.handle_api_error import handle_api_error
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(1)

async def get_family_group_api(token, msisdn):
    async with service_rate_limiter:
        service = "get_family_group_api"
        service_data = f"{service}_data"
        result = {"msisdn": msisdn}
        
        url = f"{MOLI_BASE_URL}/moli-account/v1/family-group/{msisdn}"
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    response.raise_for_status()
                    payload = await response.json()

                    # print("🛠️ get_family_group_api Payload:", data)

                    data = payload if isinstance(payload, dict) else {}

                    familyGroup = data.get("familyGroup", [{}])[0]

                    extracted_data = {
                        "msisdn": msisdn, 
                        "telco": data.get("telco", "N/A"),
                        "familyGroupId": data.get("familyGroupId", "N/A"),
                        "totalFamilyMember": data.get("totalFamilyMember", "N/A"),
                        "familyGroupLevel": familyGroup.get("familyGroupLevel", "N/A"),
                    }

                    print(f"✅ get_family_group_api: {response.status} {msisdn} {extracted_data['telco']} {extracted_data['familyGroupLevel']} TotalMembers: {extracted_data['totalFamilyMember']} FamilyID: {extracted_data['familyGroupId']} ")

                    result[service_data] = {
                        "Status": f"✅ {response.status}",
                        **extracted_data,
                    }
                    return result

        except aiohttp.ClientResponseError as error:
            return await handle_api_error(error, msisdn, service)

        except Exception as error:
            return await handle_api_error(error, msisdn, service)
        
        return result