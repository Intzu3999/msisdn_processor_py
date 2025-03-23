import os
import aiohttp
from services.auth import get_access_token

async def put_checkBlacklist_api(msisdn):
    result = {"idNo": msisdn}

    try:
        token = await get_access_token()
    except Exception as error:
        print(f"❌ Failed to fetch token: {error}")
        return result

    print(f"Successfully called checkBlacklist API with {msisdn}")
    result= {
        "msisdn": msisdn
    }

    return result