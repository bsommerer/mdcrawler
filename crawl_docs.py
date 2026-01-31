#!/usr/bin/env python3
import argparse
import sys

from mdcrawler.cli import run
from mdcrawler.crawler import derive_prefix


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Crawl documentation pages into Markdown.")
    parser.add_argument("--start-url", required=True, help="Starting URL for the crawl.")
    parser.add_argument(
        "--prefix",
        help="URL prefix to limit crawling. Defaults to start URL without last segment.",
    )
    parser.add_argument(
        "--output",
        default="output",
        help="Output directory for generated Markdown files.",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=4,
        help="Number of concurrent fetch threads.",
    )
    parser.add_argument(
        "--include-images",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Include images (including background images) in the output Markdown.",
    )
    parser.add_argument(
        "--blacklist",
        default="navigation,sidebar,contents,toolbar,pagination,footer",
        help="Comma-separated list of strings not allowed in class/id attributes.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    prefix = args.prefix or derive_prefix(args.start_url)
    return run(
        start_url=args.start_url,
        prefix=prefix,
        output_dir=args.output,
        threads=args.threads,
        include_images=args.include_images,
        blacklist=args.blacklist.split(",") if args.blacklist else [],
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
