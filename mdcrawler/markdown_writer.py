from __future__ import annotations

from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

from mdcrawler.crawler import Page


def write_pages(pages: Iterable[Page], output_dir: Path) -> None:
    pages_dir = output_dir / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    for page in pages:
        slug = _slugify(page.url)
        path = pages_dir / f"{slug}.md"
        path.write_text(page.markdown, encoding="utf-8")


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
