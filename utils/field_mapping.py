def extract_fields_from_response(data, field_mapping, service):
    """
    Extracts required fields dynamically from API response data.
    Supports nested field extraction.
    """
    extracted_data = {}
    
    for key, path in field_mapping.items():
        value = data  # Start from the top level of JSON

        try:
            # If path is a list, traverse the JSON structure
            for subkey in path:
                if isinstance(value, list):  # Handle list case (e.g., data[0])
                    value = value[0].get(subkey, "N/A") if value else "N/A"
                else:
                    value = value.get(subkey, "N/A")

            extracted_data[key] = value
        except (AttributeError, IndexError, KeyError, TypeError):
            extracted_data[key] = "N/A"

    return extracted_data

FIELD_MAP = {
    "get_customer_api": {
        "customerStatus": ["customerStatus"],
        "idNo": ["idNo"],
        "idType": ["idType"],
        "countryCode": ["countryCode"],
    },
    "get_subscriber_api": {
        "customerStatus": ["customerStatus"],
        "telco": ["telco"],
        "activeDate": ["activeDate"],
        "payType": ["payType"],
        "isPrincipal": ["isPrincipal"],
        "status": ["status"],
        "subscriptionName": ["subscriptionName"],
        "customerType": ["customerType"],
        "subscriberType": ["subscriberType"],
        "telecomType": ["telecomType"],
        "tenure": ["tenure"],
    },
    "get_account_structure_api": {
        "customerStatus": ["customerStatus"],
        "accountId": ["accountId"],
        "billingCycle": ["billingCycle"],
    },
    "get_contract_api": {
        "customerStatus": ["customerStatus"],
        "msisdn": ["msisdn"],
        "telco": ["telco"],
        "productType": ["productType"],
        "productName": ["productName"],
        "startDate": ["startDate"],
        "status": ["status"],
    },
}