# Contributing to MDCrawler

## Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mdcrawler
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

### Running Tests
```bash
pytest tests -v
```

### Code Formatting
```bash
make format
```

### Linting
```bash
make lint
```

### Running All Checks
```bash
make check
```

## Pull Request Process

1. Create a feature branch
2. Make your changes
3. Ensure all checks pass (`make check`)
4. Commit with a descriptive message
5. Open a Pull Request

## Code Style

- **black** for formatting (line length: 100)
- **ruff** for linting
- Type hints everywhere
- Docstrings for public functions
