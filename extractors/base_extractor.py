from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """Abstract base class for data extractors."""

    @abstractmethod
    def extract_data(self, service: str, data: dict, field_mapping: dict) -> dict:
        """
        Extracts relevant fields from API response data.

        :param service: The service name (e.g., 'get_customer_api').
        :param data: Raw API response data.
        :param field_mapping: Dictionary specifying which fields to extract.
        :return: Dictionary with extracted fields.
        """
        pass
