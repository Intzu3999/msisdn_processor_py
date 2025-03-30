import os
import aiohttp
from core.handle_api_error import handle_api_error
from services.base_service import BaseService
from services.service_registry import ServiceRegistry
from asyncio import Semaphore

MOLI_BASE_URL = os.getenv("MOLI_BASE_URL")

service_rate_limiter = Semaphore(1)

class GetCustomerAPIService(BaseService):
    """Service class to fetch customer details from API."""

    async def fetch_data(self, token: str, msisdn: str) -> dict:
        async with service_rate_limiter:
            service = "get_customer_api"
            result = {"msisdn": msisdn}

            api_url = f"{MOLI_BASE_URL}/moli-customer/v3/customer?msisdn={msisdn}"

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(api_url, headers=headers) as response:
                        response.raise_for_status()
                        payload = await response.json()

                        # Ensure it's a list and not empty
                        data = payload[0] if isinstance(payload, list) and payload else {}

                        personal_info = data.get("personalInfo", [{}])[0]  # First entry in list
                        identification = personal_info.get("identification", [{}])[0]  # First entry in list
                        contact_info = data.get("contact", {})  # Dictionary
                        address = contact_info.get("address", [{}])[0]  # First entry in list

                        extracted_data = {
                            "idNo": identification.get("idNo", "N/A"),
                            "idType": identification.get("type", {}).get("code", "N/A"),
                            "addressLine1": address.get("addressLine1", "N/A"),
                            "addressLine2": address.get("addressLine2", "N/A"),
                            "addressLine3": address.get("addressLine3", "N/A"),
                            "postcode": address.get("postCode", "N/A"),  # ✅ Fixed incorrect key
                            "city": address.get("city", "N/A"),
                            "state": address.get("state", {}).get("code", "N/A"),
                            "countryCode": address.get("country", {}).get("code", "N/A"),
                        }

                        print(f"✅ {service}: {response.status} {msisdn} id:{extracted_data['idType']} {extracted_data['idNo']} countryCode:{extracted_data['countryCode']}")

                        result[f"{service}_data"] = {
                            "customerStatus": f"✅ {response.status}",
                            **extracted_data,
                        }

            except (aiohttp.ClientResponseError, Exception) as error:
                return await handle_api_error(error, msisdn, service)

            return result

# Auto-register the service
ServiceRegistry.register("get_customer_api", GetCustomerAPIService)