from extractors.extractor_registry import ExtractorRegistry
from extractors.base_extractor import BaseExtractor

class GetContractExtractor(BaseExtractor):
    """Extractor for customer API data."""

    def extract_data(self, service: str, data: dict, field_mapping: dict) -> dict:
        """
        Extracts customer-related fields from API response.

        :param service: The service name.
        :param data: Raw API response data.
        :param field_mapping: Dictionary specifying which fields to extract.
        :return: Dictionary with extracted fields.
        """
        extracted_data = {}
        for key, path in field_mapping.items():
            value = data
            try:
                for subkey in path:
                    value = value.get(subkey, "N/A") if isinstance(value, dict) else "N/A"
                extracted_data[key] = value
            except AttributeError:
                extracted_data[key] = "N/A"

        return extracted_data

# Auto-register the extractor
ExtractorRegistry.register("get_customer_api", GetContractExtractor)