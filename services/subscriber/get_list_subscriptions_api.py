import os
import aiohttp

async def get_listSubscriptions_api(token, id_no):
    result = {"idNo": id_no}

    print(f"Successfully called listSubscriptions API with {id_no}")
    result= {
        "idNo": id_no
    }

    return result