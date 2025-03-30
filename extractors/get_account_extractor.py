from extractors.extractor_registry import ExtractorRegistry
from extractors.base_extractor import BaseExtractor

class GetAccountExtractor(BaseExtractor):
    """Extractor for subscriber API data."""

    def extract_data(self, service: str, data: dict, field_mapping: dict) -> dict:
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
ExtractorRegistry.register("get_customer_api", GetAccountExtractor)