import os
import aiohttp
from services.auth import get_access_token

async def get_accountStructure_api(msisdn):
    result = {"msisdn": msisdn}

    print(f"Successfully called accountStructure API with {msisdn}")
    result= {
        "idNo": msisdn
    }

    return result