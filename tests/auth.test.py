import asyncio
import sys
import os

# Get the parent directory of the current script and add it to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import services
from services.auth import get_access_token

def ():
    """Test the get_access_token function without using pytest"""
    
    # Create and use a new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        # Run the async function
        token = loop.run_until_complete(get_access_token())

        # Perform assertions
        assert isinstance(token, str), "❌ Test failed: Token is not a string"
        assert len(token) > 10, "❌ Test failed: Token length is too short"
        
        print("✅ Test passed: Token fetched successfully!")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")

    finally:
        # Always close the event loop to avoid resource leaks
        loop.close()

# Run the test
if __name__ == "__main__":
    test_get_access_token()
