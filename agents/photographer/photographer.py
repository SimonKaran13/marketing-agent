from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from typing import Iterable, List, Optional

from PIL import Image
from google import genai

@dataclass
class GeminiImage:
    image: Image.Image
    mime_type: str = "image/png"

    def to_payload(self) -> dict:
        buffer = BytesIO()
        try:
            format_hint = "PNG"
            if self.mime_type == "image/jpeg":
                format_hint = "JPEG"
            self.image.save(buffer, format=format_hint)
            return {
                "mime_type": self.mime_type,
                "data": buffer.getvalue(),
            }
        finally:
            buffer.close()


class GeminiPhotographer:
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.5-flash",
        *,
        candidate_count: int = 4,
        aspect_ratio: Optional[str] = None,
        request_options: Optional[dict] = None,
    ) -> None:
        self._model_name = model_name
        self._candidate_count = candidate_count
        self._aspect_ratio = aspect_ratio
        genai.configure(api_key=api_key)
        self._client = genai.GenerativeModel(model_name)
        self._request_options = request_options or {}

    def generate_images(
        self,
        prompt: str,
        reference_images: Iterable[GeminiImage],
    ) -> List[Image.Image]:
        if not prompt.strip():
            raise ValueError("Prompt must not be empty when requesting image generation.")

        references = [
            reference if isinstance(reference, GeminiImage) else GeminiImage(reference)  # type: ignore[arg-type]
            for reference in reference_images
        ]
        if not references:
            raise ValueError("At least one reference image is required.")

        parts: List[dict] = [{"text": prompt}]
        parts.extend(reference.to_payload() for reference in references)

        generation_config = {
            "candidate_count": self._candidate_count,
        }

        if self._aspect_ratio:
            generation_config["aspect_ratio"] = self._aspect_ratio

        response = self._client.generate_content(
            parts,
            generation_config=generation_config,
            **self._request_options,
        )

        images: List[Image.Image] = []
        for candidate in response.candidates or []:
            if candidate.content is None:
                continue
            for part in candidate.content.parts:
                inline_data = getattr(part, "inline_data", None)
                if not inline_data or not inline_data.data:
                    continue
                mime_type = inline_data.mime_type or "image/png"
                if not mime_type.startswith("image/"):
                    continue
                buffer = BytesIO(inline_data.data)
                image = Image.open(buffer)
                image.load()
                buffer.close()
                images.append(image)

        if not images:
            raise RuntimeError("No images were returned by Gemini 2.5 Flash.")

        return images