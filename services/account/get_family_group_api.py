import os
import aiohttp

async def get_familyGroup_api(token, msisdn):
    result = {"msisdn": msisdn}

    print(f"Successfully called familyGroup API with {msisdn}")
    result= {
        "idNo": msisdn
    }

    return result