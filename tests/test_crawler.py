from dataclasses import dataclass

import pytest

import mdcrawler.crawler as crawler_module


@dataclass
class FakeResponse:
    text: str


def test_crawler_recurses_and_visits_discovered_urls(monkeypatch: pytest.MonkeyPatch) -> None:
    pages = {
        "https://example.com/docs/start": """
            <html><body><p><a href="/docs/child">Child</a></p></body></html>
        """,
        "https://example.com/docs/child": """
            <html><body><p>Child page</p></body></html>
        """,
    }

    def fake_fetch(url: str) -> FakeResponse:
        return FakeResponse(text=pages[url])

    monkeypatch.setattr(crawler_module, "fetch_url", fake_fetch)

    crawler = crawler_module.Crawler(
        start_url="https://example.com/docs/start",
        prefix="https://example.com/docs/",
        threads=2,
        include_images=False,
        tag_blacklist=[],
        attr_blacklist=[],
    )
    results = crawler.run()

    urls = {page.url for page in results}
    assert urls == {
        "https://example.com/docs/start",
        "https://example.com/docs/child",
    }
