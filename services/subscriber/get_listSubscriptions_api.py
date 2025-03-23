import os
import aiohttp
from services.auth import get_access_token

async def get_listSubscriptions_api(id_no):
    result = {"idNo": id_no}

    print(f"Successfully called listSubscriptions API with {id_no}")
    result= {
        "idNo": id_no
    }

    return result