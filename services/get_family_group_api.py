import os
import aiohttp
from services.base_service import BaseService
from services.service_registry import ServiceRegistry

class GetFamilyGroupAPIService(BaseService):

    async def fetch_data(self, token: str, msisdn: str) -> dict:
        result = {"msisdn": msisdn}

        print(f"Successfully called familyGroup API with {msisdn}")
        result= {
            "idNo": msisdn
        }

        return result
    
# Auto-register the service
ServiceRegistry.register("get_family_group_api", GetFamilyGroupAPIService)