from __future__ import annotations

import logging
from dataclasses import dataclass
from io import BytesIO
from typing import Iterable, List, Optional

from PIL import Image
from google import genai
from google.genai import errors, types


logger = logging.getLogger(__name__)

@dataclass
class GeminiImage:
    image: Image.Image
    mime_type: str = "image/png"

    def to_bytes(self) -> bytes:
        buffer = BytesIO()
        try:
            format_hint = "PNG"
            if self.mime_type == "image/jpeg":
                format_hint = "JPEG"
            self.image.save(buffer, format=format_hint)
            return buffer.getvalue()
        finally:
            buffer.close()


class GeminiPhotographer:
    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-2.5-flash-image-preview",
        *,
        candidate_count: int = 4,
        aspect_ratio: Optional[str] = None,
        request_options: Optional[dict] = None,
    ) -> None:
        self._model_name = model_name
        self._candidate_count = candidate_count
        self._aspect_ratio = aspect_ratio
        self._client = genai.Client(api_key=api_key)
        if request_options is None:
            self._request_options: dict = {}
        elif isinstance(request_options, types.GenerateContentConfig):
            self._request_options = request_options.model_dump(exclude_none=True)
        else:
            self._request_options = dict(request_options)

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

        user_parts: List[types.Part] = [types.Part.from_text(text=prompt)]
        if self._aspect_ratio:
            user_parts.append(
                types.Part.from_text(
                    text=(
                        f"Please ensure the generated images use an aspect ratio of {self._aspect_ratio}."
                    )
                )
            )
        for index, reference in enumerate(references, start=1):
            reference_bytes = reference.to_bytes()
            buffer = BytesIO(reference_bytes)
            try:
                upload = self._client.files.upload(
                    file=buffer,
                    config=types.UploadFileConfig(
                        display_name=f"reference-{index}",
                        mime_type=reference.mime_type,
                    ),
                )
            finally:
                buffer.close()

            file_uri = upload.uri or upload.name
            if not file_uri:
                raise RuntimeError("Uploaded reference image is missing a file URI.")

            user_parts.append(
                types.Part.from_uri(
                    file_uri=file_uri,
                    mime_type=upload.mime_type or reference.mime_type,
                )
            )

        config_kwargs = {key: value for key, value in dict(self._request_options).items() if value is not None}
        config_kwargs.setdefault("response_modalities", ["IMAGE"])

        def _call_generate(kwargs: dict) -> types.GenerateContentResponse:
            config = types.GenerateContentConfig(**kwargs) if kwargs else None
            return self._client.models.generate_content(
                model=self._model_name,
                contents=[types.Content(role="user", parts=user_parts)],
                config=config,
            )

        try:
            response = _call_generate(config_kwargs)
        except errors.ClientError as error:
            candidate_count = config_kwargs.get("candidate_count")
            if (
                candidate_count
                and candidate_count > 1
                and "Multiple candidates is not enabled" in str(error)
            ):
                fallback_kwargs = dict(config_kwargs)
                fallback_kwargs["candidate_count"] = 1
                logger.info(
                    "Model %s does not support multiple candidates; retrying with a single image.",
                    self._model_name,
                )
                response = _call_generate(fallback_kwargs)
            else:
                raise

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
