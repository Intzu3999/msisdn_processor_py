import os
import aiohttp
from services.auth import get_access_token

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

async def get_customer_api(msisdn):
    result = {"msisdn": msisdn}
    
    try:
        token = await get_access_token()
    except Exception as error:
        print(f"❌ Failed to fetch token: {error}")
        return result  # Return empty result

    #THERE IS ANOTHER APPROAH: ISOLATE THE URL AND PARAMS AND PATH.
    # get_customer_params = {"msisdn": msisdn}
    # get_customer_url = f"{MOLI_BASE_URL}/moli-customer/v3/customer"
    # THEN, AT aiohttp.ClientSession() ADD: params=get_customer_params) as response:
    get_customer_url = f"{MOLI_BASE_URL}/moli-customer/v3/customer?msisdn={msisdn}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                get_customer_url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
            ) as response:

                response.raise_for_status()
                data = await response.json()

                id_no = data[0]["personalInfo"][0]["identification"][0].get("idNo", "N/A")
                id_type = data[0]["personalInfo"][0]["identification"][0]["type"].get("code", "NA")
                country_code = data[0]["contact"]["address"][0]["country"].get("code", "NA")

                print(f"✅ get_customer_api: {response.status} {msisdn} id:{id_type} {id_no} countryCode:{country_code}")

                result["getCustomerApiData"] = {
                    "customerStatus": f"✅ {response.status}",
                    "idNo": id_no,
                    "idType": id_type,
                    "countryCode": country_code,
                }

    except aiohttp.ClientResponseError as error:
        print(f"❌ get_customer_api: Status - {error.status}, Error - {error.message}")
        result["getCustomerApiData"] = f"❌ {error.status}"

    except Exception as error:
        print(f"❌ Error fetching customer API: {error}")
        result["getCustomerApiData"] = "❌ Unknown Error"

    return result