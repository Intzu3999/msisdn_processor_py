import subprocess

csv_file = "test"
services = [
    "get_account_structure_api",
    "get_contract_api",
    "get_customer_api",
    "get_subscriber_api",
    "open_orders_api",
]

for service in services:
    command = f"python read_csv.py {csv_file} --service {service}"
    print(f"Executing: {command}")

    process = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")
    
    print(process.stdout)
    print(process.stderr)