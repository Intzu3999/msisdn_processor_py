from services.get_customer_api import get_customer_api, get_contract_api, put_check_blacklist_api
from services.get_subscriber_api import get_subscriber_api
from services.get_account_api import get_account_structure_api
from services.get_open_orders_api import get_open_orders_api
from services.get_postpaid_validation_api import get_postpaid_validation_api

SERVICE_MAPPING = {
    "get_customer_api": get_customer_api,
    "get_contract_api": get_contract_api,
    "get_subscriber_api": get_subscriber_api,
    "get_account_structure_api": get_account_structure_api,
    "get_open_orders_api": get_open_orders_api,
    "get_postpaid_validation_api": get_postpaid_validation_api,
}

def get_service_function(service):
    service_function = SERVICE_MAPPING.get(service)
    if not service_function:
        print(f"⚠️ Warning: '{service}' is not mapped in SERVICE_MAPPING.")
    return service_function