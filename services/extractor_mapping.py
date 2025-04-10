def extract_flattenned_data(service, data, field_mapping):
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

def extract_another_data_structure(service, data, field_mapping):
    extracted_data = {}
    # Logic to extract_another_data_structure
    return extracted_data

def extract_nested_data(service, data, field_mapping):
    extracted_data = {}
    # Logic to extract extract_nested_data
    return extracted_data

EXTRACTOR_MAPPING = {
"get_account_structure_api": extract_flattenned_data,
"get_contract_api": extract_flattenned_data,
"get_customer_api": extract_flattenned_data,
"get_subscriber_api": extract_flattenned_data,
"open_orders_api": extract_flattenned_data,
"postpaid_validation_api": extract_flattenned_data,
"account_structure_api": extract_flattenned_data,
}

def get_service_extractor_function(service, data, field_mapping):
    extractor_function = EXTRACTOR_MAPPING.get(service)
    if not extractor_function:
        print(f"⚠️ Warning: '{service}' is not mapped in EXTRACTOR_MAPPING.")
    return extractor_function