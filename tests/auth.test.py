import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from services.auth import get_access_token

def test_get_access_token ():
    """Test the get_access_token function without using pytest"""
    
    # Create and use a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        token = loop.run_until_complete(get_access_token())

        assert isinstance(token, str), "❌ Test failed"
        assert len(token) > 10, "❌ Test failed"
        
        print("✅ Test passed")

    except Exception as e:
        print(f"❌ Test failed: {e}")

    finally:
        # Always close the event loop to avoid resource leaks
        loop.close()

if __name__ == "__main__":
    test_get_access_token()
