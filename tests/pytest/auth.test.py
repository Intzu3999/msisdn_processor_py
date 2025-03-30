import asyncio
from services.auth import get_access_token

def test_get_access_token():
    loop = asyncio.new_event_loop() 
    asyncio.set_event_loop(loop)
    token = loop.run_until_complete(get_access_token())
    loop.close() 

    assert isinstance(token, str) and len(token) > 10, "❌ Test failed"
    print("✅ Test passed")

test_get_access_token()