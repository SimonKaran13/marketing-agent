#!/usr/bin/env python3
"""Interactive test runner for the Gemini photographer agent."""

import os
import sys
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from PIL import Image

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
    HEIF_SUPPORTED = True
except ImportError:  # pragma: no cover - optional dependency
    HEIF_SUPPORTED = False

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from agents.photographer.photographer import GeminiImage, GeminiPhotographer  # noqa: E402
from prompts.InputPrompt import InputPrompt  # noqa: E402
from utils.img_requirement_processor import process_img_requirement  # noqa: E402


def prompt_for_text(label: str) -> Optional[str]:
    """Collect a free-form text attribute from the user."""
    value = input(f"{label} (press Enter to skip): \n> ").strip()
    return value or None


def prompt_for_list(label: str) -> Optional[List[str]]:
    """Collect a comma-separated list from the user, returning None when empty."""
    raw = input(f"{label} (comma-separated, Enter to skip): \n> ").strip()
    if not raw:
        return None
    items = [item.strip() for item in raw.split(",") if item.strip()]
    return items or None


def load_reference_images(paths: List[str]) -> List[GeminiImage]:
    """Open each image path and wrap it in a GeminiImage."""
    references: List[GeminiImage] = []
    for raw_path in paths:
        path = Path(raw_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Reference image not found: {path}")

        suffix = path.suffix.lower()
        if suffix in {".heic", ".heif"} and not HEIF_SUPPORTED:
            raise RuntimeError(
                "HEIC/HEIF support not available. Install pillow-heif (pip install pillow-heif) to load these files."
            )

        with Image.open(path) as img:
            image_copy = img.convert("RGB") if img.mode not in {"RGB", "RGBA"} else img.copy()
            fmt = (img.format or "PNG").upper()

        if fmt in {"JPG", "JPEG"}:
            mime = "image/jpeg"
        elif fmt in {"HEIF", "HEIC"}:
            mime = "image/png"
        else:
            mime = "image/png"

        references.append(GeminiImage(image=image_copy, mime_type=mime))

    return references


def collect_input_prompt(image_paths: List[str]) -> InputPrompt:
    """Interactively gather the attributes required for InputPrompt."""
    print("\nPlease provide details about the product to enrich the photography prompt.")

    kwargs = {
        "product_images": image_paths,
        "product_name": prompt_for_text("Product name"),
        "product_description": prompt_for_text("Product description"),
        "product_main_features": prompt_for_text("Key features"),
        "product_benefits": prompt_for_text("Key benefits"),
        "product_use_cases": prompt_for_text("Primary use cases"),
        "product_pricing": prompt_for_text("Pricing summary"),
        "product_pricing_details": prompt_for_text("Pricing details"),
        "product_pricing_features": prompt_for_text("Pricing features"),
        "product_pricing_benefits": prompt_for_text("Pricing benefits"),
        "product_target_audience": prompt_for_text("Target audience"),
        "background_scene": prompt_for_text("Preferred background scene"),
        "composition_style": prompt_for_text("Composition style"),
        "lighting_preferences": prompt_for_text("Lighting preferences"),
        "mood": prompt_for_text("Desired mood"),
        "camera_setup": prompt_for_text("Camera setup"),
        "color_palette": prompt_for_text("Color palette"),
        "additional_modifiers": prompt_for_text("Additional modifiers"),
        "style_presets": prompt_for_list("Style presets"),
        "format_presets": prompt_for_list("Format presets"),
        "shot_presets": prompt_for_list("Shot presets"),
        "lighting_presets": prompt_for_list("Lighting presets"),
        "camera_angle_presets": prompt_for_list("Camera angle presets"),
        "lens_presets": prompt_for_list("Lens presets"),
        "environment_presets": prompt_for_list("Environment presets"),
        "color_grade_presets": prompt_for_list("Color grade presets"),
        "post_processing_presets": prompt_for_list("Post-processing presets"),
    }

    return InputPrompt(**kwargs)


def main() -> None:
    print("🧪 Gemini Photographer Interactive Test")
    print("=" * 45)

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY is required. Add it to your environment or .env file.")

    raw_paths = input(
        "Enter reference image path(s) (absolute or relative). Use commas for multiple files:\n> "
    ).strip()
    if not raw_paths:
        raise ValueError("At least one reference image path must be provided.")

    image_paths = [path.strip() for path in raw_paths.split(",") if path.strip()]
    reference_images = load_reference_images(image_paths)

    prompt_data = collect_input_prompt(image_paths)
    prompt_text = process_img_requirement(prompt_data)

    print("\nGenerated prompt for Gemini:")
    print("-" * 45)
    print(prompt_text)
    print("-" * 45)

    photographer = GeminiPhotographer(api_key=api_key)

    print("\nRequesting image generation from Gemini... This may take a moment.")
    images = photographer.generate_images(prompt_text, reference_images)
    print(f"Received {len(images)} candidate images.")

    output_dir = Path("generated_photos")
    output_dir.mkdir(parents=True, exist_ok=True)

    for idx, image in enumerate(images, start=1):
        output_path = output_dir / f"gemini_photo_{idx}.png"
        image.save(output_path)
        print(f"Saved candidate #{idx} -> {output_path}")

    print("\n✅ Test run complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTest aborted by user.")
