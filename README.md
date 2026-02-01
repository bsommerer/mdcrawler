# MDCrawler

[![CI](https://github.com/bsommerer/mdcrawler/actions/workflows/test.yml/badge.svg)](https://github.com/bsommerer/mdcrawler/actions/workflows/test.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

---

> 🕷️ **Crawl any documentation site. Get clean Markdown. Feed it to your LLM.**

A command-line tool that crawls documentation websites and converts them to clean Markdown files. Useful for creating offline documentation, feeding docs to LLMs, or archiving web content.

## Features

- Recursively crawls all pages under a URL prefix
- Converts HTML to clean Markdown (headings, lists, tables, code blocks, inline formatting)
- Filters out navigation, sidebars, footers, and other non-content elements
- Optionally downloads and includes images
- Concurrent fetching for faster crawling
- Generates both individual page files and a combined single-file output

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd mdcrawler

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package
pip install -e .

# Or with development dependencies (for contributing)
pip install -e ".[dev]"
```

## Usage

### Basic usage

```bash
mdcrawler --start-url https://docs.example.com/guide/intro
```

This will:
1. Start crawling from the given URL
2. Follow all links under `https://docs.example.com/guide/`
3. Save Markdown files to the `output/` directory

### With all options

```bash
mdcrawler \
  --start-url https://docs.example.com/guide/intro \
  --prefix https://docs.example.com/guide/ \
  --output ./my-docs \
  --threads 8 \
  --include-images \
  --tag-blacklist nav,aside,footer,script,style \
  --attr-blacklist sidebar,navigation,toolbar
```

## CLI Options

| Option | Default | Description |
|--------|---------|-------------|
| `--start-url` | (required) | The URL to start crawling from |
| `--prefix` | auto | URL prefix to limit crawling scope. Only pages starting with this prefix are crawled. Defaults to start URL without the last path segment |
| `--output` | `output` | Directory where Markdown files are saved |
| `--threads` | `4` | Number of concurrent fetch threads |
| `--include-images` | disabled | Download images and include them in Markdown output |
| `--no-include-images` | (default) | Do not include images |
| `--tag-blacklist` | `nav,aside,footer,form,button,input,textarea,select,noscript,script,style,svg,iframe` | HTML tags to exclude (content inside these tags is removed) |
| `--attr-blacklist` | `navigation,sidebar,contents,toolbar,pagination,footer,absolute` | Strings to match against class/id attributes for exclusion |

## Output Structure

```
output/
├── combined.md          # All pages combined into one file
├── index.md             # Table of contents with links
├── images/              # Downloaded images (if --include-images)
│   ├── docs-example-com-logo.png
│   └── docs-example-com-hero.jpg
└── pages/               # Individual page files
    ├── docs-example-com-guide-intro.md
    ├── docs-example-com-guide-setup.md
    └── docs-example-com-guide-api.md
```

## Examples

### Crawl Python documentation

```bash
mdcrawler \
  --start-url https://docs.python.org/3/tutorial/index.html \
  --prefix https://docs.python.org/3/tutorial/
```

### Crawl with images

```bash
mdcrawler \
  --start-url https://docs.example.com/guide/intro \
  --include-images \
  --output ./docs-with-images
```

### Fast crawl with more threads

```bash
mdcrawler \
  --start-url https://docs.example.com/guide/intro \
  --threads 16
```

### Custom filtering

```bash
# Exclude additional elements
mdcrawler \
  --start-url https://docs.example.com/guide/intro \
  --tag-blacklist nav,aside,footer,script,style,svg,iframe,form \
  --attr-blacklist sidebar,navigation,toolbar,toc,breadcrumb
```

## Development

### Running Tests

```bash
make test
# or
pytest tests/ -v
```

### Code Quality

```bash
make format   # Auto-format code
make lint     # Run linters (ruff, black, mypy)
make check    # Run all checks (lint + test)
```

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Fetch     │────▶│   Extract   │────▶│   Convert   │────▶│   Output    │
│   HTML      │     │   Content   │     │ to Markdown │     │   Files     │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │                   │
      ▼                   ▼                   ▼                   ▼
  Concurrent          Removes nav,       Headings, lists,    Individual +
  fetching            sidebars, etc.     tables, code        combined .md
```

1. **Fetching**: Fetches HTML pages concurrently using the specified number of threads
2. **Extraction**: Parses HTML with BeautifulSoup and extracts main content
3. **Filtering**: Removes blacklisted tags and elements matching blacklisted class/id patterns
4. **Conversion**: Converts remaining HTML to Markdown (headings, lists, tables, code blocks, inline formatting)
5. **Link Discovery**: Finds internal links within the prefix scope for recursive crawling
6. **Output**: Writes individual Markdown files and a combined file with all content

---

<p align="center">
  Made with ❤️ and 🐍 Python
  <br>
  <sub>Built with BeautifulSoup • Powered by concurrent.futures</sub>
</p>
