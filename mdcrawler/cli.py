from __future__ import annotations

from pathlib import Path

from mdcrawler.combined_builder import build_combined
from mdcrawler.crawler import Crawler
from mdcrawler.markdown_writer import write_index, write_pages
from mdcrawler.title_normalizer import normalize_titles


def run(
    start_url: str,
    prefix: str,
    output_dir: str,
    threads: int,
    include_images: bool,
    blacklist: list[str],
) -> int:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    crawler = Crawler(
        start_url=start_url,
        prefix=prefix,
        threads=threads,
        include_images=include_images,
        blacklist=blacklist,
    )
    pages = crawler.run()
    if not pages:
        return 1

    normalized_titles = normalize_titles([page.title for page in pages])
    for page, normalized in zip(pages, normalized_titles):
        page.title = normalized

    write_pages(pages, output_path)
    write_index(pages, output_path, start_url=start_url)
    build_combined(pages, output_path)
    return 0
