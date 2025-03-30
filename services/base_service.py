from abc import ABC, abstractmethod

class BaseService(ABC):
    """Abstract base class for API services."""

    @abstractmethod
    async def fetch_data(self, token: str, msisdn: str) -> dict:
        """
        Fetch data from the API.

        :param token: Authentication token for API request.
        :param msisdn: The MSISDN (phone number) to query.
        :return: Dictionary containing API response data.
        """
        pass
