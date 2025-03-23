import os
import aiohttp
from services.auth import get_access_token

async def get_subscriber_api(id_no):
    result = {"idNo": id_no}

    print(f"Successfully called subscriber API with {id_no}")
    result= {
        "idNo": id_no
    }

    return result