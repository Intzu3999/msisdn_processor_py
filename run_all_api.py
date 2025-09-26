import subprocess

csv_file = "temp"
services = [
    "get_account_structure_api",
    # "get_contract_api",
    "get_customer_api",
    "get_subscriber_api",
    "get_open_orders_api",
    "get_family_group_api",
    # "get_postpaid_validation_api",
]

for service in services:
    command = f"python run_api.py {csv_file} --service {service}"
    print(f"Executing: {command}")

    process = subprocess.run(command, shell=True, capture_output=True, text=True, encoding="utf-8")
    
    print(process.stdout)
    print(process.stderr)