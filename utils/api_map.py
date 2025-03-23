from services.customer.get_customer_api import get_customer_api
from services.customer.put_check_blacklist_api import put_check_blacklist_api
from services.subscriber.get_subscriber_api import get_subscriber_api
from services.account.get_account_structure_api import get_account_structure_api

api_map = {
    "get_customer_api": get_customer_api,
    "get_subscriber_api": get_subscriber_api,
    "get_account_structure_api": get_account_structure_api,
    "put_check_blacklist_api": put_check_blacklist_api,
}