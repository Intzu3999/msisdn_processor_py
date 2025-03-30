import sys
import os
import asyncio
import aiohttp
import pandas as pd
import argparse
from mappings.field_mapping import FIELD_MAPPING
from services.service_registry import ServiceRegistry
from extractors.extractor_registry import ExtractorRegistry
from services.auth import get_access_token
from utils.datetime_utils import date_with_time
from dotenv import load_dotenv


sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

parser = argparse.ArgumentParser(description="Process CSV & API calls.")
parser.add_argument("filename", nargs="?", default="test", help="CSV file name (without extension)")
parser.add_argument("--service", default="get_customer_api", help="API service to run")
args = parser.parse_args()

CSV_PATH = os.path.join(os.path.dirname(__file__), "dataStream", f"{args.filename}.csv")
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "results")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, f"{args.filename}-{args.service}-{date_with_time()}.xlsx")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

async def process_data():
    """Reads CSV, processes API calls, and saves results."""
    try:
        df = pd.read_csv(CSV_PATH)
        print(f"[OK] CSV loaded: {CSV_PATH}")

    except FileNotFoundError:
        print(f"[FAIL] Error: File '{args.filename}.csv' not found.")
        return
    except Exception as e:
        print(f"[FAIL] Error reading CSV: {e}")
        return

    results = [] # Pandas new DataFrame
    tasks = [] # Panda's way process for each row asynchronously

    token = await get_access_token()

    for index, row in df.iterrows():
        msisdn = row["msisdn"]
        tasks.append(fetch_api_data(token, msisdn, index, results, args.service))

    await asyncio.gather(*tasks)

    save_results_to_excel(results)

async def fetch_api_data(token, msisdn, index, results, service):
    try:
        import services.get_customer_api
        print(f"🔍 Registered services: {ServiceRegistry._services.keys()}")

        service_class = ServiceRegistry.get_service(service)
        if not service_class:
            print(f"⚠️ Warning: API '{service}' is not registered.")
            return
        
        service_instance = service_class()
        response = await service_instance.fetch_data(token, msisdn)

        import extractors.get_customer_extractor
        print(f"🔍 Registered extractors: {ExtractorRegistry._extractors.keys()}")

        extractor_class = ExtractorRegistry.get_extractor(service)
        if not extractor_class:
            print(f"⚠️ Warning: Extractor for '{service}' is not registered.")
            return
        
        extractor_instance = extractor_class()

        field_mapping = FIELD_MAPPING.get(service, {})
        print(f"🔍 Field mapping for '{service}': {field_mapping}")

        extracted_data = extractor_instance.extract_data(service, response, field_mapping)
        print(f"🔍 Extracted data for {msisdn}: {extracted_data}")
        
        result_entry = {"msisdn": msisdn, **extracted_data} # Always include msisdn
        results.append(result_entry)      

    except Exception as e:
        print(f"❌ Error processing {msisdn}: {e}")
 
def save_results_to_excel(results):
    df_results = pd.DataFrame(results)

    try:
        df_results.to_excel(OUTPUT_FILE, index=False, engine="openpyxl")
        print(f"Results saved: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error saving results: {e}")

if __name__ == "__main__":
    asyncio.run(process_data())