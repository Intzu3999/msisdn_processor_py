from typing import Type, Dict
from services.base_service import BaseService

class ServiceRegistry:
    """Registry to dynamically register and retrieve API services."""
    
    _services: Dict[str, Type[BaseService]] = {} # class-level storage, stores registered services in a dictionary

    @classmethod
    def register(cls, service_name: str, service_class: Type[BaseService]):
        """Dynamically registers a service class under a given name."""
        cls._services[service_name] = service_class # uses class-level storage
        print(f"✅ Service registered: {service_name} -> {service_class}")

    @classmethod
    def get_service(cls, service_name: str) -> Type[BaseService] | None:
        """Dynamically retrieves a service class under a given name."""
        return cls._services.get(service_name) # uses class-level storage
    