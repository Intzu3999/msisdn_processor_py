import sys
import os
import asyncio
import pandas as pd
import argparse
from services.auth import get_access_token
from services.extractor_mapping import get_service_extractor_function
from services.xlsx_field_mapping import XLSX_FIELD_MAPPING
from services.service_mapping import get_service_function
from utils.datetime_utils import date_with_time
from dotenv import load_dotenv


sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

parser = argparse.ArgumentParser(description="Process CSV & API calls.")
parser.add_argument("filename", nargs="?", default="test", help="CSV file name (without extension)")
parser.add_argument("--service", default="get_subscriber_api", help="API service to run")
args = parser.parse_args()

CSV_PATH = os.path.join(os.path.dirname(__file__), "dataStream", f"{args.filename}.csv")
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "results")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, f"{args.filename}-{args.service}-{date_with_time()}.xlsx")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

async def process_data():
    """Reads CSV, processes API calls, and saves results."""
    try:
        df = pd.read_csv((CSV_PATH), dtype={"msisdn": int})
        print(f"[OK] CSV loaded: {CSV_PATH}")

    except FileNotFoundError:
        print(f"[FAIL] Error: File '{args.filename}.csv' not found.")
        return
    except Exception as e:
        print(f"[FAIL] Error reading CSV: {e}")
        return

    results = [] # Pandas new DataFrame
    tasks = [] # Panda's way process for each row asynchronously

    # try:
    # token = os.getenv("ACCESS_TOKEN")
    # except:
    token = await get_access_token()
    # print(token)

    for index, row in df.iterrows():
        msisdn = int(row["msisdn"])
        tasks.append(fetch_api_data(token, msisdn, index, results, args.service))

    await asyncio.gather(*tasks)

    save_results_to_excel(results)

async def fetch_api_data(token, msisdn, index, results, service):
    try:
        service_function = get_service_function(service)
        response = await service_function(token, msisdn)

        service_data = f"{service}_data"
        data = response.get(service_data, {})

        xlsx_field_mapping = XLSX_FIELD_MAPPING.get(service, {})
        
        extractor_function = get_service_extractor_function(service, data, xlsx_field_mapping)
        extracted_data = extractor_function(service, data, xlsx_field_mapping)

        # will be able to handle both list and dict
        if isinstance(extracted_data, list):
            for item in extracted_data:
                results.append({"msisdn": msisdn, **item})
        else:
            results.append({"msisdn": msisdn, **extracted_data})

        # result_entry = {"msisdn": msisdn, **extracted_data}
        # results.append(result_entry)      

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
