import base64
from io import BytesIO

from PIL import Image


def decode_image_base64(image_base64: str) -> bytes:
    if image_base64.startswith("data:image/"):
        image_base64 = image_base64.split(",", 1)[1]
    return base64.b64decode(image_base64, validate=False)


def image_data_url(image_base64: str) -> str:
    """Build a vision API data URL with the correct MIME type."""
    if image_base64.startswith("data:image/"):
        return image_base64

    raw = decode_image_base64(image_base64)
    normalized = _normalize_for_vision(raw)
    return f"data:{normalized['mime_type']};base64,{normalized['base64']}"


def _normalize_for_vision(raw: bytes) -> dict[str, str]:
    """Resize large screenshots so vision requests do not hang on huge images."""
    try:
        with Image.open(BytesIO(raw)) as image:
            image = image.convert("RGB")
            image.thumbnail((1800, 1800))

            output = BytesIO()
            image.save(output, format="JPEG", quality=88, optimize=True)
            return {
                "mime_type": "image/jpeg",
                "base64": base64.b64encode(output.getvalue()).decode("utf-8"),
            }
    except Exception:
        return {
            "mime_type": _detect_mime_type(raw),
            "base64": base64.b64encode(raw).decode("utf-8"),
        }


def _detect_mime_type(raw: bytes) -> str:
    if raw.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if raw.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if raw.startswith(b"GIF87a") or raw.startswith(b"GIF89a"):
        return "image/gif"
    if raw.startswith(b"RIFF") and raw[8:12] == b"WEBP":
        return "image/webp"
    return "image/jpeg"
