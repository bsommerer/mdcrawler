from __future__ import annotations

from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from urllib.parse import urlsplit, urlunsplit

from mdcrawler.content_extractor import ImageReference, extract_content
from mdcrawler.fetcher import fetch_url


@dataclass
class Page:
    url: str
    title: str
    markdown: str
    images: list[ImageReference]


def derive_prefix(start_url: str) -> str:
    parts = urlsplit(start_url)
    path = parts.path.rstrip("/")
    if "/" in path:
        path = path.rsplit("/", 1)[0] + "/"
    else:
        path = "/"
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


class Crawler:
    def __init__(self, start_url: str, prefix: str, threads: int = 4, include_images: bool = False) -> None:
        self.start_url = start_url
        self.prefix = prefix
        self.threads = max(1, threads)
        self.include_images = include_images
        self.visited: set[str] = set()
        self.lock = threading.Lock()

    def run(self) -> list[Page]:
        with self.lock:
            self.visited.add(self.start_url)
        pages: list[Page] = []

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._crawl_url, self.start_url): self.start_url}
            while futures:
                for future in as_completed(list(futures)):
                    futures.pop(future, None)
                    result = future.result()
                    if result is None:
                        continue
                    page, discovered = result
                    if page.markdown.strip():
                        pages.append(page)
                    for url in discovered:
                        if self._mark_visited(url):
                            futures[executor.submit(self._crawl_url, url)] = url

        return pages

    def _mark_visited(self, url: str) -> bool:
        with self.lock:
            if url in self.visited:
                return False
            self.visited.add(url)
            return True

    def _crawl_url(self, url: str) -> tuple[Page, list[str]] | None:
        try:
            response = fetch_url(url)
        except Exception:
            return None
        content = extract_content(response.text, url, self.prefix, include_images=self.include_images)
        page = Page(url=url, title=content.title, markdown=content.markdown, images=content.images)
        return page, content.discovered_urls
