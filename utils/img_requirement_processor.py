from typing import Iterable, List, Optional, Union

from prompts.InputPrompt import InputPrompt

TextSource = Optional[Union[str, Iterable[str]]]


def _sanitize(text: Optional[str]) -> str:
    return " ".join(text.strip().split()) if text else ""


def _collect_phrases(*sources: TextSource) -> List[str]:
    phrases: List[str] = []
    for source in sources:
        if not source:
            continue
        if isinstance(source, str):
            candidates = [piece.strip() for piece in source.split(",") if piece.strip()]
        else:
            candidates: List[str] = []
            for item in source:
                if not item:
                    continue
                if isinstance(item, str):
                    candidates.extend(piece.strip() for piece in item.split(",") if piece.strip())
                else:
                    text = str(item).strip()
                    if text:
                        candidates.append(text)
        for candidate in candidates:
            if candidate and candidate not in phrases:
                phrases.append(candidate)
    return phrases


def process_img_requirement(input_prompt: InputPrompt) -> str:
    if not input_prompt.product_images:
        raise ValueError("InputPrompt.product_images must contain at least one reference image.")

    product_name = _sanitize(input_prompt.product_name) or "the product"
    description = _sanitize(input_prompt.product_description)
    features = _sanitize(input_prompt.product_main_features)
    benefits = _sanitize(input_prompt.product_benefits)
    use_cases = _sanitize(input_prompt.product_use_cases)
    pricing = _sanitize(input_prompt.product_pricing)
    pricing_details = _sanitize(input_prompt.product_pricing_details)
    pricing_features = _sanitize(input_prompt.product_pricing_features)
    pricing_benefits = _sanitize(input_prompt.product_pricing_benefits)
    target_audience = _sanitize(input_prompt.product_target_audience)

    environment_tags = _collect_phrases(input_prompt.environment_presets)
    background_scene = (
        _sanitize(input_prompt.background_scene)
        or use_cases
        or (environment_tags[0] if environment_tags else "a clean, contemporary setting")
    )

    subject = f"{product_name}, {description}" if description else product_name

    style_tags = _collect_phrases(
        input_prompt.style_presets,
        input_prompt.composition_style,
        input_prompt.mood,
        input_prompt.additional_modifiers,
    )

    lighting_tags = _collect_phrases(
        input_prompt.lighting_preferences,
        input_prompt.lighting_presets,
    )

    camera_tags = _collect_phrases(
        input_prompt.camera_setup,
        input_prompt.camera_angle_presets,
        input_prompt.lens_presets,
    )

    color_tags = _collect_phrases(
        input_prompt.color_palette,
        input_prompt.color_grade_presets,
    )

    format_tags = _collect_phrases(
        input_prompt.format_presets,
        input_prompt.shot_presets,
    )

    post_process_tags = _collect_phrases(input_prompt.post_processing_presets)

    narrative_tags = _collect_phrases(target_audience)
    if pricing:
        narrative_tags.append(pricing)
    if pricing_details:
        narrative_tags.append(pricing_details)

    supporting_details: List[str] = []
    if features:
        supporting_details.append(f"Highlight key features: {features}.")
    if benefits:
        supporting_details.append(f"Showcase benefits: {benefits}.")

    value_tags = _collect_phrases(pricing_features, pricing_benefits)
    if value_tags:
        supporting_details.append(f"Reinforce value proposition: {', '.join(value_tags)}.")

    if narrative_tags:
        supporting_details.append(f"Align messaging with {', '.join(narrative_tags)}.")

    if environment_tags:
        supporting_details.append(f"Environment cues: {', '.join(environment_tags)}.")

    if lighting_tags:
        supporting_details.append(f"Lighting: {', '.join(lighting_tags)}.")

    if camera_tags:
        supporting_details.append(f"Camera and lens: {', '.join(camera_tags)}.")

    if style_tags:
        supporting_details.append(f"Styling cues: {', '.join(style_tags)}.")

    if format_tags:
        supporting_details.append(f"Framing preferences: {', '.join(format_tags)}.")

    if color_tags:
        supporting_details.append(f"Color treatment: {', '.join(color_tags)}.")

    if post_process_tags:
        supporting_details.append(f"Post-processing: {', '.join(post_process_tags)}.")

    prompt_lines = [
        f"Create a professional product photograph of {subject}.",
        f"Set the scene in {background_scene}.",
    ]

    prompt_lines.extend(supporting_details)

    prompt_lines.append(
        "Use the provided reference imagery only to preserve authentic form, materials, and branding without revealing the originals."
    )

    return "\n".join(prompt_lines)
