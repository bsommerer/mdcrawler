from __future__ import annotations

import argparse
from pathlib import Path

from mdcrawler.combined_builder import build_combined
from mdcrawler.content_extractor import DEFAULT_ATTR_BLACKLIST, DEFAULT_TAG_BLACKLIST
from mdcrawler.crawler import Crawler, derive_prefix
from mdcrawler.markdown_writer import write_index, write_pages
from mdcrawler.title_normalizer import normalize_titles


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for mdcrawler command."""
    parser = _build_parser()
    args = parser.parse_args(argv)
    prefix = args.prefix or derive_prefix(args.start_url)

    tag_blacklist = (
        [t.strip() for t in args.tag_blacklist.split(",") if t.strip()]
        if args.tag_blacklist
        else None
    )
    attr_blacklist = (
        [a.strip() for a in args.attr_blacklist.split(",") if a.strip()]
        if args.attr_blacklist
        else None
    )

    return run(
        start_url=args.start_url,
        prefix=prefix,
        output_dir=args.output,
        threads=args.threads,
        include_images=args.include_images,
        tag_blacklist=tag_blacklist,
        attr_blacklist=attr_blacklist,
    )


def _build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(description="Crawl documentation pages into Markdown.")
    parser.add_argument("--start-url", required=True, help="Starting URL for the crawl.")
    parser.add_argument(
        "--prefix",
        help="URL prefix to limit crawling. Defaults to start URL without last segment.",
    )
    parser.add_argument("--output", default="output", help="Output directory.")
    parser.add_argument("--threads", type=int, default=4, help="Concurrent fetch threads.")
    parser.add_argument(
        "--include-images",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Include images (including background images) in the output Markdown.",
    )
    parser.add_argument(
        "--tag-blacklist",
        default=",".join(DEFAULT_TAG_BLACKLIST),
        help=(
            "Comma-separated list of HTML tags to exclude. "
            f"Default: {','.join(DEFAULT_TAG_BLACKLIST)}"
        ),
    )
    parser.add_argument(
        "--attr-blacklist",
        default=",".join(DEFAULT_ATTR_BLACKLIST),
        help=(
            "Comma-separated list of strings to match against class/id attributes. "
            f"Default: {','.join(DEFAULT_ATTR_BLACKLIST)}"
        ),
    )
    return parser


def run(
    start_url: str,
    prefix: str,
    output_dir: str,
    threads: int,
    include_images: bool,
    tag_blacklist: list[str] | None,
    attr_blacklist: list[str] | None,
) -> int:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    crawler = Crawler(
        start_url=start_url,
        prefix=prefix,
        threads=threads,
        include_images=include_images,
        tag_blacklist=tag_blacklist,
        attr_blacklist=attr_blacklist,
    )
    pages = crawler.run()
    if not pages:
        return 1

    normalized_titles = normalize_titles([page.title for page in pages])
    for page, normalized in zip(pages, normalized_titles, strict=True):
        page.title = normalized

    write_pages(pages, output_path)
    write_index(pages, output_path, start_url=start_url)
    build_combined(pages, output_path)
    return 0
