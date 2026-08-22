#!/usr/bin/env python3
from __future__ import annotations

import base64
import mimetypes
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "index.with-assets.html"
OUTPUT = ROOT / "index.html"
CSS = ROOT / "assets" / "css" / "styles.css"
JS = ROOT / "assets" / "js" / "storefront.js"
INLINE_IMAGE_ROOT = Path("/private/tmp/dihworld-inline-images")

IMAGE_MAP = {
    "assets/images/dihworld-audio-logo.jpg": INLINE_IMAGE_ROOT / "dihworld-audio-logo.jpg",
    "assets/images/dihworld-disk-image.png": INLINE_IMAGE_ROOT / "dihworld-disk-image.jpg",
    "../images/dihworld-disk-image.png": INLINE_IMAGE_ROOT / "dihworld-disk-image.jpg",
    "assets/images/sacredverb.png": INLINE_IMAGE_ROOT / "sacredverb.jpg",
    "assets/images/cathedral.png": INLINE_IMAGE_ROOT / "cathedral.jpg",
    "assets/images/debo.png": INLINE_IMAGE_ROOT / "debo.jpg",
    "assets/images/drumkrushglue.png": INLINE_IMAGE_ROOT / "drumkrushglue.jpg",
    "assets/images/mariana.png": INLINE_IMAGE_ROOT / "mariana.jpg",
    "assets/images/ui-sacredverb.jpg": ROOT / "assets" / "images" / "ui-sacredverb.jpg",
    "assets/images/ui-cathedral.jpg": ROOT / "assets" / "images" / "ui-cathedral.jpg",
    "assets/images/ui-debo.jpg": ROOT / "assets" / "images" / "ui-debo.jpg",
    "assets/images/ui-mariana.jpg": ROOT / "assets" / "images" / "ui-mariana.jpg",
}


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def resolve_image(original: str, preferred_path: Path) -> Path:
    if preferred_path.exists():
        return preferred_path

    repo_relative = original.replace("../images/", "assets/images/")
    repo_path = ROOT / repo_relative
    if repo_path.exists():
        return repo_path

    raise FileNotFoundError(f"Missing inline image: {preferred_path}")


def main() -> None:
    html = SOURCE.read_text(encoding="utf-8")
    css = CSS.read_text(encoding="utf-8")
    js = JS.read_text(encoding="utf-8")

    for original, image_path in IMAGE_MAP.items():
        replacement = data_uri(resolve_image(original, image_path))
        html = html.replace(original, replacement)
        css = css.replace(original, replacement)

    html = html.replace('    <link rel="stylesheet" href="assets/css/styles.css">\n', f"    <style>\n{css}\n    </style>\n")
    html = html.replace('    <script src="assets/js/storefront.js"></script>', f"    <script>\n{js}\n    </script>")

    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
