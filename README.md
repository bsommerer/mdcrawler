# MDCrawler

## CLI usage

```bash
python crawl_docs.py --start-url https://example.com/docs/intro.html --output output
```

Optional flags:

- `--prefix`: URL prefix to limit crawling (defaults to the start URL without the last path segment).
- `--threads`: Number of concurrent fetch threads (default: 4).
- `--output`: Output directory for Markdown files (default: `output`).
- `--include-images` / `--no-include-images`: Include images (including background images) and save them under `images/` (default: disabled).
- `--blacklist`: Comma-separated list of class/id tokens to exclude from extraction (default: `navigation,sidebar,contents,toolbar,pagination,footer`).

## Example output structure

```
output/
├── combined.md
├── index.md
├── images/
│   ├── docs-example-com-logo.png
│   └── docs-example-com-hero.jpg
└── pages/
    ├── example-com-docs-intro-html.md
    └── example-com-docs-installation-html.md
```

## Smoke test (manual)

```bash
python crawl_docs.py \
  --start-url https://example.com/docs/intro.html \
  --output output \
  --threads 4
```

Confirm that `output/index.md`, `output/combined.md`, and at least one file in `output/pages/` were created.
