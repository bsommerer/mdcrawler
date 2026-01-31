from __future__ import annotations

from dataclasses import dataclass
from queue import Queue
import threading
from urllib.parse import urlsplit, urlunsplit

from mdcrawler.content_extractor import ImageReference, extract_content
from mdcrawler.fetcher import fetch_urls


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
        self.queue: Queue[str] = Queue()
        self.visited: set[str] = set()
        self.lock = threading.Lock()

    def run(self) -> list[Page]:
        with self.lock:
            self.visited.add(self.start_url)
            self.queue.put(self.start_url)
        pages: list[Page] = []

        while True:
            batch: list[str] = []
            while len(batch) < self.threads and not self.queue.empty():
                batch.append(self.queue.get())

            if not batch:
                break

            results = fetch_urls(batch, self.threads)
            for url, response in results:
                if response is None:
                    continue
                content = extract_content(response.text, url, self.prefix, include_images=self.include_images)
                if content.markdown.strip():
                    pages.append(
                        Page(url=url, title=content.title, markdown=content.markdown, images=content.images)
                    )
                self._enqueue_discovered(content.discovered_urls)

        return pages

    def _enqueue_discovered(self, urls: list[str]) -> None:
        with self.lock:
            for url in urls:
                if url in self.visited:
                    continue
                self.visited.add(url)
                self.queue.put(url)
