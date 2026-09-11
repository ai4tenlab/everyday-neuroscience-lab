#!/usr/bin/env python3
"""Fail-closed validation for Everyday Neuroscience Lab generated thumbnails.

Use after image_generate has returned a local PNG/WebP path and after copying it
into assets/images/thumbnails/. This does not generate or alter an image.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, UnidentifiedImageError

MIN_WIDTH = 1200
MIN_HEIGHT = 675
MIN_RATIO = 1.70  # accepts standard 16:9 output with small encoder rounding
MAX_RATIO = 1.82
ALLOWED_FORMATS = {"PNG", "WEBP", "JPEG"}


def fail(message: str) -> int:
    print(f"THUMBNAIL_VALIDATION=fail\nreason={message}")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a 16:9-ish blog thumbnail before committing it."
    )
    parser.add_argument("image", type=Path, help="Path to a generated thumbnail")
    args = parser.parse_args()
    path = args.image

    if not path.is_file():
        return fail(f"missing_file:{path}")
    if path.stat().st_size < 50_000:
        return fail(f"file_too_small:{path.stat().st_size}_bytes")

    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            fmt = image.format
            width, height = image.size
    except (UnidentifiedImageError, OSError) as exc:
        return fail(f"unreadable_image:{exc}")

    if fmt not in ALLOWED_FORMATS:
        return fail(f"unsupported_format:{fmt}")
    if width < MIN_WIDTH or height < MIN_HEIGHT:
        return fail(f"undersized:{width}x{height}")

    ratio = width / height
    if not MIN_RATIO <= ratio <= MAX_RATIO:
        return fail(f"aspect_ratio:{ratio:.4f}_expected_16_9")

    print(
        "THUMBNAIL_VALIDATION=pass\n"
        f"path={path}\nformat={fmt}\ndimensions={width}x{height}\n"
        f"aspect_ratio={ratio:.4f}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
