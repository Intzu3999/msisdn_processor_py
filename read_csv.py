import os
import asyncio
import aiohttp
import pandas as pd
import argparse
from dotenv import load_dotenv
from utils.field_mapping import FIELD_MAP, extract_fields_from_response
from utils.api_map import api_map

load_dotenv()

parser = argparse.ArgumentParser(description="Process CSV & API calls.")
parser.add_argument("filename", nargs="?", default="test", help="CSV file name (without extension)")
parser.add_argument("--service", default="get_customer_api", help="API service to run")
args = parser.parse_args()

CSV_PATH = os.path.join(os.path.dirname(__file__), "dataStream", f"{args.filename}.csv")
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "results")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, f"{args.service}.xlsx")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

async def process_data():
    """Reads CSV, processes API calls, and saves results."""
    try:
        df = pd.read_csv(CSV_PATH)
        print(f"✅ CSV loaded: {CSV_PATH}")

    except FileNotFoundError:
        print(f"❌ Error: File '{args.filename}.csv' not found.")
        return
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return

    results = [] # Pandas new DataFrame
    tasks = [] # Panda's way process for each row asynchronously

    for index, row in df.iterrows():
        msisdn = row["msisdn"]
        tasks.append(fetch_api_data(msisdn, index, results, args.service))

    await asyncio.gather(*tasks)

    save_results_to_excel(results)

async def fetch_api_data(msisdn, index, results, service):
    try:
        if service not in api_map:
            print(f"⚠️ Warning: API '{service}' is not mapped.")
            return

        api_func = api_map[service]
        response = await api_func(msisdn)

        service_data = f"{service}_data"
        data = response.get(service_data, {})

        field_mapping = FIELD_MAP.get(service, {})
        extracted_data = extract_fields_from_response(data, field_mapping, service)

        result_entry = {"msisdn": msisdn, **extracted_data} # Always include msisdn
        results.append(result_entry)      

    except Exception as e:
        print(f"❌ Error processing {msisdn}: {e}")

def save_results_to_excel(results):
    """Save processed customer data to an Excel file."""
    df_results = pd.DataFrame(results)

    try:
        df_results.to_excel(OUTPUT_FILE, index=False, engine="openpyxl")
        print(f"💾 Results saved successfully: {OUTPUT_FILE}")
    except Exception as e:
        print(f"❌ Error saving results: {e}")

if __name__ == "__main__":
    asyncio.run(process_data())