#!/usr/bin/env python3
"""Fail-closed local + live verification for a 뉴로시민 daily post.

This script is intentionally dependency-free so another Hermes node can use it
immediately after cloning the repository. It never publishes or sends email.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

SITE = "https://ai4tenlab.github.io/everyday-neuroscience-lab"


def fail(reason: str) -> int:
    print(f"DAILY_PUBLICATION_VERIFICATION=fail\nreason={reason}")
    return 1


def fetch(url: str) -> tuple[int, str]:
    request = urllib.request.Request(url, headers={"User-Agent": "EverydayNeuroscienceLabVerifier/1.1"})
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")
    except urllib.error.URLError as exc:
        raise RuntimeError(str(exc.reason)) from exc


def front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise ValueError("missing_front_matter")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify today's local and live daily post.")
    parser.add_argument("--date", default=date.today().isoformat(), help="YYYY-MM-DD, default: local today")
    parser.add_argument("--skip-live", action="store_true", help="Only validate repository files")
    args = parser.parse_args()

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        return fail("invalid_date")
    posts = sorted(Path("_posts").glob(f"{args.date}-*.md"))
    if len(posts) != 1:
        return fail(f"expected_exactly_one_post_found_{len(posts)}")
    post = posts[0]
    try:
        fields = front_matter(post)
    except (OSError, ValueError) as exc:
        return fail(f"front_matter:{exc}")

    for required in ("title", "permalink", "image", "image_alt", "source_url"):
        if not fields.get(required):
            return fail(f"missing_front_matter:{required}")
    image_path = Path(fields["image"].lstrip("/"))
    validate = subprocess.run(
        [sys.executable, "scripts/validate_thumbnail.py", str(image_path)],
        text=True, capture_output=True, check=False,
    )
    if validate.returncode != 0:
        return fail("thumbnail_validation:" + validate.stdout.replace("\n", ";").strip())

    post_text = post.read_text(encoding="utf-8")
    if "application/ld+json" not in post_text:
        return fail("missing_json_ld")
    if args.skip_live:
        print(f"DAILY_PUBLICATION_VERIFICATION=pass\npost={post}\nmode=local_only")
        return 0

    permalink = fields["permalink"].strip("/")
    post_url = f"{SITE}/{permalink}/"
    image_url = f"{SITE}/{fields['image'].lstrip('/')}"
    try:
        post_status, html = fetch(post_url)
        image_status, _ = fetch(image_url)
    except RuntimeError as exc:
        return fail(f"network:{exc}")
    if post_status != 200:
        return fail(f"post_http:{post_status}")
    if image_status != 200:
        return fail(f"image_http:{image_status}")
    expected_og = f'content="{image_url}"'
    if expected_og not in html or 'name="twitter:card" content="summary_large_image"' not in html:
        return fail("missing_live_social_metadata")
    if "post-thumbnail" not in html:
        return fail("missing_live_thumbnail")

    print(
        "DAILY_PUBLICATION_VERIFICATION=pass\n"
        f"post={post}\nurl={post_url}\nimage_url={image_url}\n"
        f"thumbnail={validate.stdout.splitlines()[-1]}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
