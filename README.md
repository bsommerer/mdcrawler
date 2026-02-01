<p align="center">
  <img src="https://img.shields.io/badge/🕷️-MDCRAWLER-blueviolet?style=for-the-badge&labelColor=black" alt="MDCrawler"/>
</p>

<h1 align="center">🕷️ MDCrawler</h1>

<p align="center">
  <strong>The World's Most Advanced Documentation Harvesting System™</strong>
</p>

<p align="center">
  <em>Trusted by mass-market developers worldwide*</em>
</p>

<p align="center">
  <a href="https://github.com/bsommerer/mdcrawler/actions/workflows/test.yml"><img src="https://github.com/bsommerer/mdcrawler/actions/workflows/test.yml/badge.svg" alt="CI"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue.svg" alt="Python 3.10+"></a>
  <a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://mypy-lang.org/"><img src="https://www.mypy-lang.org/static/mypy_badge.svg" alt="Checked with mypy"></a>
  <a href="http://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/blazingly-fast-orange?style=flat-square" alt="Blazingly Fast">
  <img src="https://img.shields.io/badge/zero-dependencies*-green?style=flat-square" alt="Zero Dependencies">
  <img src="https://img.shields.io/badge/powered%20by-AI%20vibes-purple?style=flat-square" alt="AI Vibes">
  <img src="https://img.shields.io/badge/works-on%20my%20machine-blue?style=flat-square" alt="Works on my machine">
  <img src="https://img.shields.io/badge/bugs-features-red?style=flat-square" alt="Bugs are Features">
</p>

---

<p align="center">
  <strong>🚀 REVOLUTIONARY • 💡 INNOVATIVE • 🔥 DISRUPTIVE • 🧠 AI-READY</strong>
</p>

> ### 🕷️ *"Crawl any documentation site. Get clean Markdown. Feed it to your LLM. Change the world."*

<p align="center">
  <a href="docs/whitepaper.pdf"><img src="https://img.shields.io/badge/📄_Read_the-Whitepaper-informational?style=for-the-badge" alt="Read the Whitepaper"></a>
</p>

<p align="center">
  <sub>
    <strong>Peer-reviewed*</strong> technical whitepaper available:
    <a href="docs/whitepaper.pdf"><em>"MDCrawler: A Revolutionary Paradigm Shift in Documentation Harvesting Technology"</em></a>
    <br>
    Sommerer, B. (2026). MDCrawler Industries Technical Report. DOI: 10.xxxx/notreal.2026
  </sub>
</p>

---

## 🌟 Why MDCrawler?

While other tools are still trying to figure out how to parse HTML, **MDCrawler** has already:

- 🏆 **Redefined** what it means to crawl documentation
- 🚀 **Disrupted** the web scraping industry
- 🧠 **Pioneered** LLM-ready documentation harvesting
- ⚡ **Achieved** unprecedented levels of Markdown purity
- 🎯 **Revolutionized** the developer experience

<details>
<summary><strong>📊 Impressive Statistics That Will Blow Your Mind</strong></summary>

| Metric | Value |
|--------|-------|
| Lines of Code | **~850** (yes, that's all it takes to change the world) |
| Test Coverage | **We have tests** |
| Stars | ⭐ (yours could be the first!) |
| Downloads | **Incalculable** |
| Industry Awards | **Pending** |
| Carbon Footprint | **Probably fine** |

</details>

---

## ✨ Features That Will Make You Cry (Happy Tears)

<table>
<tr>
<td width="50%">

### 🕸️ Intelligent Crawling
Our **state-of-the-art** recursive crawling engine uses advanced algorithms (for loops) to discover every page.

</td>
<td width="50%">

### ⚡ Blazingly Fast™
Powered by `concurrent.futures` - the same technology used by... other Python projects!

</td>
</tr>
<tr>
<td width="50%">

### 🧹 Smart Filtering
AI-inspired blacklist technology (if statements) removes unwanted content with surgical precision.

</td>
<td width="50%">

### 📝 Pure Markdown
Converts HTML to Markdown so clean, you could eat off it. (Please don't.)

</td>
</tr>
<tr>
<td width="50%">

### 🖼️ Image Harvesting
Downloads images because sometimes words aren't enough to express documentation.

</td>
<td width="50%">

### 📦 Zero Config*
Works out of the box! Just provide a URL. And a prefix. And maybe some options.

</td>
</tr>
</table>

---

## 🚀 Quick Start (Your Life Will Never Be The Same)

```bash
# Install this masterpiece
pip install -e .

# Experience documentation enlightenment
mdcrawler --start-url https://docs.python.org/3/tutorial/

# Witness the magic ✨
ls output/
```

**That's it.** You've just joined the revolution.

---

## 💻 Installation

```bash
# Clone the repository (you're making history)
git clone <repository-url>
cd mdcrawler

# Create a virtual environment (best practices matter)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install and ascend to a higher plane of existence
pip install -e .

# Want to contribute to greatness?
pip install -e ".[dev]"
```

---

## 🎮 Usage

### The Simple Way (For Mortals)

```bash
mdcrawler --start-url https://docs.example.com/guide/intro
```

### The Power User Way (For Legends)

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

### The "I Read The Docs" Way (Maximum Respect)

| Option | Default | Description |
|--------|---------|-------------|
| `--start-url` | (required) | The URL where your journey begins |
| `--prefix` | auto | URL prefix to limit crawling scope |
| `--output` | `output` | Where the magic happens |
| `--threads` | `4` | Parallel universe threads |
| `--include-images` | disabled | Harvest the visuals too |
| `--tag-blacklist` | *sensible defaults* | HTML tags to banish |
| `--attr-blacklist` | *sensible defaults* | Classes/IDs to eliminate |

---

## 📁 Output Structure (Artisanally Crafted)

```
output/
├── combined.md          # 📖 The Tome of All Knowledge
├── index.md             # 🗂️ Your Table of Contents
├── images/              # 🖼️ Visual Treasures
│   ├── logo.png
│   └── hero.jpg
└── pages/               # 📄 Individual Scrolls of Wisdom
    ├── intro.md
    ├── setup.md
    └── api.md
```

---

## 🏗️ Architecture (Enterprise-Grade™)

```
                            ╔═══════════════════════════════════════╗
                            ║      M D C R A W L E R   v0.1.0       ║
                            ║   "It's not a bug, it's a feature"    ║
                            ╚═══════════════════════════════════════╝
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    │                         │                         │
                    ▼                         ▼                         ▼
           ┌───────────────┐         ┌───────────────┐         ┌───────────────┐
           │   🌐 FETCH    │         │   🔬 EXTRACT  │         │   📝 CONVERT  │
           │               │         │               │         │               │
           │  requests +   │────────▶│ BeautifulSoup │────────▶│   Markdown    │
           │  threading    │         │    magic      │         │   alchemy     │
           └───────────────┘         └───────────────┘         └───────────────┘
                    │                         │                         │
                    │                         │                         │
                    ▼                         ▼                         ▼
           ┌─────────────────────────────────────────────────────────────────┐
           │                        💾 OUTPUT                                │
           │                                                                 │
           │   combined.md  +  index.md  +  pages/*.md  +  images/*         │
           │                                                                 │
           │                    "Pure. Markdown. Bliss."                     │
           └─────────────────────────────────────────────────────────────────┘
```

---

## 🧪 Development (Join The Elite)

```bash
# Run tests (we have them!)
make test

# Format code (beauty matters)
make format

# Lint everything (quality is not negotiable)
make lint

# The full experience
make check
```

---

## 🎯 Real-World Examples

### 📚 Crawl Python Docs (Classic)
```bash
mdcrawler \
  --start-url https://docs.python.org/3/tutorial/index.html \
  --prefix https://docs.python.org/3/tutorial/
```

### 🖼️ Crawl With Images (Premium Experience)
```bash
mdcrawler \
  --start-url https://docs.example.com/guide/intro \
  --include-images \
  --output ./docs-with-images
```

### ⚡ Speed Run (16 Threads, No Mercy)
```bash
mdcrawler \
  --start-url https://docs.example.com/guide/intro \
  --threads 16
```

---

## 🤝 Contributing

We welcome contributions from developers who understand true greatness.

1. Fork it
2. Branch it (`git checkout -b feature/amazing-feature`)
3. Commit it (`git commit -m 'Add amazing feature'`)
4. Push it (`git push origin feature/amazing-feature`)
5. PR it

See [CONTRIBUTING.md](CONTRIBUTING.md) for the sacred texts.

---

## 📜 License

MIT - Because sharing is caring.

---

## 🙏 Acknowledgments

- **BeautifulSoup** - For making HTML bearable
- **Requests** - For making HTTP human
- **Python** - For existing
- **Coffee** - For making this possible
- **You** - For reading this far

---

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-❤️%20and%20🐍-red?style=for-the-badge" alt="Made with love and Python">
</p>

<p align="center">
  <strong>Built with BeautifulSoup • Powered by concurrent.futures • Mass-market approved by masses</strong>
</p>

<p align="center">
  <sub>* "Zero dependencies" excludes dependencies. "Trusted by mass-market developers" based on mass-market self-evaluation.</sub>
</p>

<p align="center">
  <sub>© 2026 MDCrawler Industries™ - A Division of "It Works On My Machine" Enterprises</sub>
</p>
