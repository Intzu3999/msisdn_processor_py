import os
import aiohttp
from services.auth import get_access_token

async def put_barSubscriber_api(id_no):
    result = {"idNo": id_no}

    print(f"Successfully called barSubscriber API with {id_no}")
    result= {
        "idNo": id_no
    }

    return result

async def put_unbarSubscriber_api(id_no):
    result = {"idNo": id_no}

    print(f"Successfully called unbarSubscriber API with {id_no}")
    result= {
        "idNo": id_no
    }

    return result