import os
import aiohttp

async def put_barSubscriber_api(token, id_no):
    result = {"idNo": id_no}

    print(f"Successfully called barSubscriber API with {id_no}")
    result= {
        "idNo": id_no
    }

    return result

async def put_unbarSubscriber_api(token, id_no):
    result = {"idNo": id_no}

    print(f"Successfully called unbarSubscriber API with {id_no}")
    result= {
        "idNo": id_no
    }

    return result