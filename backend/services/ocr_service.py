import base64
from io import BytesIO

from PIL import Image, ImageFilter, ImageOps

from .image_utils import decode_image_base64


def extract_text_with_tesseract(image_base64: str) -> str:
    """Extract text from screenshots locally with Tesseract OCR."""
    try:
        import pytesseract
    except ImportError:
        return ""

    try:
        raw = decode_image_base64(image_base64)
        with Image.open(BytesIO(raw)) as image:
            prepared = _prepare_for_ocr(image)
            text = pytesseract.image_to_string(
                prepared,
                config="--oem 3 --psm 6",
            )
            return _clean_ocr_text(text)
    except Exception as e:
        print(f"Tesseract OCR failed: {e}")
        return ""


def _prepare_for_ocr(image: Image.Image) -> Image.Image:
    image = ImageOps.exif_transpose(image)
    image = image.convert("L")

    # Screenshots often have small text. Upscale before thresholding.
    width, height = image.size
    scale = 2 if max(width, height) < 2200 else 1
    if scale > 1:
        image = image.resize((width * scale, height * scale), Image.Resampling.LANCZOS)

    image = ImageOps.autocontrast(image)
    image = image.filter(ImageFilter.SHARPEN)
    image = image.point(lambda pixel: 255 if pixel > 175 else 0)
    return image


def _clean_ocr_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]
    return "\n".join(lines)
