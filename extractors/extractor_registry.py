from typing import Type, Dict
from extractors.base_extractor import BaseExtractor

class ExtractorRegistry:
    """Registry to dynamically register and retrieve extractors."""
    
    _extractors: Dict[str, Type[BaseExtractor]] = {} #this stores registered extractors in a dictionary

    @classmethod
    def register(cls, extractor_name: str, extractor_class: Type[BaseExtractor]):
        """Dynamically registers an extractor class under a given name."""
        cls._extractors[extractor_name] = extractor_class
        print(f"✅ Extractor registered: {extractor_name} -> {extractor_class}")

    @classmethod
    def get_extractor(cls, extractor_name: str) -> Type[BaseExtractor] | None:
        """Dynamically retrieves an extractor class by name."""
        return cls._extractors.get(extractor_name)
