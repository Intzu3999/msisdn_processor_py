import os
import aiohttp
from services.auth import get_access_token

async def get_familyGroup_api(msisdn):
    result = {"msisdn": msisdn}

    print(f"Successfully called familyGroup API with {msisdn}")
    result= {
        "idNo": msisdn
    }

    return result