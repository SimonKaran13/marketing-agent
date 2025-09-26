from dataclasses import dataclass
from typing import Optional


@dataclass
class Prompt:
    product_name: Optional[str] = None
    product_description: Optional[str] = None
    product_main_features: Optional[str] = None
    product_benefits: Optional[str] = None
    product_use_cases: Optional[str] = None
    product_pricing: Optional[str] = None
    product_pricing_details: Optional[str] = None
    product_pricing_features: Optional[str] = None
    product_pricing_benefits: Optional[str] = None