# MDCrawler

## CLI usage

```bash
python crawl_docs.py --start-url https://example.com/docs/intro.html --output output
```

Optional flags:

- `--prefix`: URL prefix to limit crawling (defaults to the start URL without the last path segment).
- `--threads`: Number of concurrent fetch threads (default: 4).
- `--output`: Output directory for Markdown files (default: `output`).

## Example output structure

```
output/
├── combined.md
├── index.md
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
