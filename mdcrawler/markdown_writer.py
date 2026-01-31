from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

import requests

from mdcrawler.content_extractor import ImageReference
from mdcrawler.crawler import Page


def write_pages(pages: Iterable[Page], output_dir: Path) -> None:
    pages_dir = output_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    images_dir = output_dir / "images"
    pages = list(pages)
    for page in pages:
        if page.images:
            images_dir.mkdir(parents=True, exist_ok=True)
            _materialize_images(page, images_dir)
        slug = _slugify(page.url)
        path = pages_dir / f"{slug}.md"
        markdown = render_markdown(page, image_prefix="../images/")
        path.write_text(markdown, encoding="utf-8")


def write_index(pages: Iterable[Page], output_dir: Path, start_url: str) -> None:
    lines = ["# Crawl Index", "", f"Start-URL: {start_url}", ""]
    for page in pages:
        slug = _slugify(page.url)
        lines.append(f"- **{page.title}** ({page.url}) -> pages/{slug}.md")
    lines.append("")
    (output_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")


def _slugify(url: str) -> str:
    parsed = urlparse(url)
    slug = parsed.netloc + parsed.path
    slug = slug.strip("/") or parsed.netloc
    slug = slug.replace("/", "-")
    slug = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in slug)
    return slug.lower()


def render_markdown(page: Page, image_prefix: str) -> str:
    markdown = page.markdown
    for image in page.images:
        if not image.filename:
            continue
        alt_text = image.alt or "Image"
        markdown = markdown.replace(image.token, f"![{alt_text}]({image_prefix}{image.filename})")
    return markdown


def _materialize_images(page: Page, images_dir: Path) -> None:
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(page.images)))) as executor:
        futures = {
            executor.submit(_download_image, image, images_dir, index): image
            for index, image in enumerate(page.images)
        }
        for future in as_completed(futures):
            future.result()


def _download_image(image: ImageReference, images_dir: Path, index: int) -> None:
    filename = _image_filename(image.url, index)
    output_path = images_dir / filename
    if output_path.exists():
        image.filename = filename
        return
    try:
        response = requests.get(image.url, timeout=15)
        response.raise_for_status()
    except requests.RequestException:
        return
    output_path.write_bytes(response.content)
    image.filename = filename


def _image_filename(url: str, index: int) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name
    if not name or "." not in name:
        name = f"image-{index}.bin"
    safe = "".join(ch if ch.isalnum() or ch in ".-_" else "-" for ch in name)
    return f"{parsed.netloc}-{safe}"
