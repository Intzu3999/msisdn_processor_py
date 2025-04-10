from services.customer.get_customer_api import get_customer_api
from services.customer.get_contract_api import get_contract_api
from services.subscriber.get_subscriber_api import get_subscriber_api
from services.account.get_account_structure_api import get_account_structure_api
from services.open_orders import open_orders_api
from services.postpaid_validation import postpaid_validation_api
from services.account_structure import account_structure_api

SERVICE_MAPPING = {
    "get_customer_api": get_customer_api,
    "get_contract_api": get_contract_api,
    "get_subscriber_api": get_subscriber_api,
    "get_account_structure_api": get_account_structure_api,
    "open_orders_api": open_orders_api,
    "postpaid_validation_api": postpaid_validation_api,
    "account_structure_api": account_structure_api,
}

def get_service_function(service):
    service_function = SERVICE_MAPPING.get(service)
    if not service_function:
        print(f"⚠️ Warning: '{service}' is not mapped in SERVICE_MAPPING.")
    return service_function