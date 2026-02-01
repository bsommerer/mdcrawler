#!/usr/bin/env python3
import argparse
import sys

from mdcrawler.cli import run
from mdcrawler.crawler import derive_prefix
from mdcrawler.content_extractor import DEFAULT_TAG_BLACKLIST, DEFAULT_ATTR_BLACKLIST


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
        "--tag-blacklist",
        default=",".join(DEFAULT_TAG_BLACKLIST),
        help=(
            "Comma-separated list of HTML tags to exclude (also excludes content within these tags). "
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


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    prefix = args.prefix or derive_prefix(args.start_url)

    tag_blacklist = [t.strip() for t in args.tag_blacklist.split(",") if t.strip()] if args.tag_blacklist else None
    attr_blacklist = [a.strip() for a in args.attr_blacklist.split(",") if a.strip()] if args.attr_blacklist else None

    return run(
        start_url=args.start_url,
        prefix=prefix,
        output_dir=args.output,
        threads=args.threads,
        include_images=args.include_images,
        tag_blacklist=tag_blacklist,
        attr_blacklist=attr_blacklist,
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
