import asyncio
from services.auth import get_access_token

def test_get_access_token():
    loop = asyncio.new_event_loop()  # Create an event loop
    asyncio.set_event_loop(loop)  # Set the event loop
    token = loop.run_until_complete(get_access_token())  # Run async function
    loop.close()  # Close event loop

    assert isinstance(token, str) and len(token) > 10, "Invalid token received"
    print("✅ Test passed: Token fetched successfully!")

test_get_access_token()
