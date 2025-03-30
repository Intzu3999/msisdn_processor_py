import os
import aiohttp
from services.base_service import BaseService
from services.service_registry import ServiceRegistry


class GetAccountAPIService(BaseService):

    async def fetch_data(self, token: str, msisdn: str) -> dict:
        result = {"msisdn": msisdn}

        print(f"Successfully called account API with {msisdn}")
        result= {
            "idNo": msisdn
        }

        return result

# Auto-register the service
ServiceRegistry.register("get_account_api", GetAccountAPIService)