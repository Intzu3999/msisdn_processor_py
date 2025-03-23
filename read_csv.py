import os
import asyncio
import pandas as pd
import argparse
from dotenv import load_dotenv
from services.customer.get_customer_api import get_customer_api
from services.customer.put_checkBlacklist_api import put_checkBlacklist_api
from services.subscriber.get_subscriber_api import get_subscriber_api
from services.account.get_accountStructure_api import get_accountStructure_api

load_dotenv()

parser = argparse.ArgumentParser(description="Process CSV & API calls.")
parser.add_argument("filename", nargs="?", default="test", help="CSV file name (without extension)")
parser.add_argument("--service", default="customer", help="API service to run")
args = parser.parse_args()

CSV_PATH = os.path.join(os.path.dirname(__file__), "dataStream", f"{args.filename}.csv")
OUTPUT_FOLDER = os.path.join(os.path.dirname(__file__), "results")
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, f"{args.service}.xlsx")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

api_map = {
    "customer": get_customer_api,
    "subscriber": get_subscriber_api,
    "accountStructure": get_accountStructure_api,
    "checkBlacklist": put_checkBlacklist_api
}

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

        http_status = response.get("getCustomerApiData", {}).get("httpStatus", "❌ Failed")
        id_no = response.get("getCustomerApiData", {}).get("idNo", "N/A")
        id_type = response.get("getCustomerApiData", {}).get("idType", "N/A")
        country_code = response.get("getCustomerApiData", {}).get("countryCode", "N/A")

        result_entry = {
            "msisdn": msisdn,
            "customerStatus": http_status,
            "idNo": id_no,
            "idType": id_type,
            "countryCode": country_code
        }


        # API CHAINING EXAMPLE
        if service == "customer" and id_no != "N/A":
            # subscriber_response = await get_subscriber_api(id_no)
            # subscriber_status = subscriber_response.get("status", "Unknown")
            subscriber_status = id_no
            result_entry["subsciberStatus"] = subscriber_status 
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
