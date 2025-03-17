try:
    import aiohttp
    from dotenv import load_dotenv
    print("✅ All imports work!")
except ImportError as e:
    print(f"❌ Import error: {e}")