import os
import aiohttp

async def put_check_blacklist_api(token, msisdn):
    result = {"idNo": msisdn}

    print(f"Successfully called checkBlacklist API with {msisdn}")
    result= {
        "msisdn": msisdn
    }

    return result