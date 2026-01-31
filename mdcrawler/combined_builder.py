from __future__ import annotations

from pathlib import Path
from typing import Iterable

from mdcrawler.crawler import Page
from mdcrawler.markdown_writer import render_markdown


def build_combined(pages: Iterable[Page], output_dir: Path) -> None:
    combined_lines: list[str] = ["# Combined Documentation", ""]
    for page in pages:
        combined_lines.append(f"## {page.title}")
        combined_lines.append("")
        markdown = render_markdown(page, image_prefix="images/")
        combined_lines.extend(_shift_headings(markdown, shift=1).splitlines())
        combined_lines.append("")
    (output_dir / "combined.md").write_text("\n".join(combined_lines).rstrip() + "\n", encoding="utf-8")


def _shift_headings(markdown: str, shift: int) -> str:
    shifted_lines: list[str] = []
    for line in markdown.splitlines():
        if line.startswith("#"):
            hashes = len(line) - len(line.lstrip("#"))
            new_hashes = min(6, hashes + shift)
            content = line.lstrip("#").lstrip()
            shifted_lines.append(f"{'#' * new_hashes} {content}".rstrip())
        else:
            shifted_lines.append(line)
    return "\n".join(shifted_lines)
