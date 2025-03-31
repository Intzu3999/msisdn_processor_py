from services.customer_api import get_customer_api, get_contract_api, put_check_blacklist_api
from services.subscriber_api import get_subscriber_api, get_list_subscriptions_api, put_bar_subscriber_api, put_unbar_subscriber_api
from services.account_api import get_account_structure_api, get_account_api, get_family_group_api

SERVICE_MAPPING = {
    "get_customer_api": get_customer_api,
    "get_contract_api": get_contract_api,
    "get_subscriber_api": get_subscriber_api,
    "get_account_structure_api": get_account_structure_api,
    "get_account_api":get_account_api,
    "get_family_group_api":get_family_group_api,
    "put_check_blacklist_api": put_check_blacklist_api,
}