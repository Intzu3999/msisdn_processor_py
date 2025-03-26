import os
import aiohttp

async def get_account_api(token, msisdn):
    result = {"msisdn": msisdn}

    print(f"Successfully called account API with {msisdn}")
    result= {
        "idNo": msisdn
    }

    return result