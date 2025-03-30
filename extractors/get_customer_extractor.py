from extractors.base_extractor import BaseExtractor
from extractors.extractor_registry import ExtractorRegistry

class GetCustomerExtractor(BaseExtractor):
    """Extractor for customer API data."""

    def extract_data(self, service: str, data: dict, field_mapping: dict) -> dict:
        extracted = {}
        for key, path in field_mapping.items():
            if isinstance(path, list):  
                path = ".".join(path)  # Convert list to a dot-separated string
            extracted[key] = self.get_nested_value(data, path.split(".")) or "N/A"
        return extracted

    def get_nested_value(self, data, keys):
        """Safely extract nested values from a dictionary."""
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, {})
            else:
                return None
        return data if data else None

# Auto-register the extractor
ExtractorRegistry.register("get_customer_api", GetCustomerExtractor)