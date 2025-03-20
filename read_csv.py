import pandas as pd
import os
import argparse

# Setup argument parser
parser = argparse.ArgumentParser(description="Read a CSV file and process API calls.")
parser.add_argument("filename", nargs="?", default="test", help="CSV file name (without extension)")
parser.add_argument("--service", default="subscriberStatus", help="API service to run")

# Parse arguments
args = parser.parse_args()

# Construct file paths dynamically
csv_path = os.path.join(os.path.dirname(__file__), "dataStream", f"{args.filename}.csv")
output_folder = os.path.join(os.path.dirname(__file__), "results")
output_file = os.path.join(output_folder, f"{args.service}.xlsx")

# Ensure the /results folder exists
os.makedirs(output_folder, exist_ok=True)

try:
    # Load CSV
    df = pd.read_csv(csv_path)
    print(f"✅ CSV file '{args.filename}.csv' loaded successfully!\n")
    print(df)

    # Save to XLSX
    df.to_excel(output_file, index=False)
    print(f"")
    print(f"💾 Saved at: {output_file}")

except FileNotFoundError:
    print(f"❌ Error: The file '{args.filename}.csv' was not found in 'dataStream'.")
except Exception as e:
    print(f"❌ Error reading the CSV: {e}")
