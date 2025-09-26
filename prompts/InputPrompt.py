from dataclasses import dataclass
from typing import Optional, List


@dataclass
class InputPrompt:
    # Stores file paths or URLs of uploaded product images (required)
    product_images: List[str]
    # "Acme Hydration Bottle"
    product_name: Optional[str] = None
    # "vacuum-insulated stainless steel water bottle"
    product_description: Optional[str] = None
    # "double-wall insulation, leakproof lid, 24oz capacity"
    product_main_features: Optional[str] = None
    # "keeps drinks cold for 24 hours, easy-carry loop"
    product_benefits: Optional[str] = None
    # "outdoor adventures, gym sessions, commute"
    product_use_cases: Optional[str] = None
    # "premium", "budget-friendly", "mid-tier"
    product_pricing: Optional[str] = None
    # "launch bundle $79 with infuser"
    product_pricing_details: Optional[str] = None
    # "includes lifetime warranty"
    product_pricing_features: Optional[str] = None
    # "save 20% with subscription"
    product_pricing_benefits: Optional[str] = None
    # "designed for eco-conscious athletes"
    product_target_audience: Optional[str] = None
    # "sunlit alpine meadow", "modern kitchen countertop"
    background_scene: Optional[str] = None
    # "rule of thirds composition", "flat lay"
    composition_style: Optional[str] = None
    # "dramatic rim lighting", "soft daylight"
    lighting_preferences: Optional[str] = None
    # "energetic", "calm and minimalist"
    mood: Optional[str] = None
    # "macro product shot", "tripod-mounted studio setup"
    camera_setup: Optional[str] = None
    # "teal and orange accents"
    color_palette: Optional[str] = None
    # Free-form comma list, "splashing water droplets, premium props"
    additional_modifiers: Optional[str] = None
    # Checkbox collections inspired by Gemini Imagen docs
    style_presets: Optional[List[str]] = None  # ["cinematic", "editorial"]
    format_presets: Optional[List[str]] = None  # ["4:5 portrait", "square"]
    shot_presets: Optional[List[str]] = None  # ["macro detail", "hero shot"]
    lighting_presets: Optional[List[str]] = None  # ["studio softbox", "golden hour"]
    camera_angle_presets: Optional[List[str]] = None  # ["low angle", "eye level"]
    lens_presets: Optional[List[str]] = None  # ["35mm prime", "85mm portrait"]
    environment_presets: Optional[List[str]] = None  # ["urban rooftop", "nature trail"]
    color_grade_presets: Optional[List[str]] = None  # ["vibrant pop", "muted pastels"]
    post_processing_presets: Optional[List[str]] = None  # ["high gloss", "film grain"]
