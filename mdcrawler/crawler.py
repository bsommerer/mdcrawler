from __future__ import annotations

from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
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
    def __init__(
        self,
        start_url: str,
        prefix: str,
        threads: int = 4,
        include_images: bool = False,
        tag_blacklist: list[str] | None = None,
        attr_blacklist: list[str] | None = None,
    ) -> None:
        self.start_url = start_url
        self.prefix = prefix
        self.threads = max(1, threads)
        self.include_images = include_images
        self.tag_blacklist = tag_blacklist
        self.attr_blacklist = attr_blacklist
        self.visited: set[str] = set()
        self.lock = threading.Lock()

    def run(self) -> list[Page]:
        with self.lock:
            self.visited.add(self.start_url)
        pages: list[Page] = []
        start_time = time.monotonic()
        processed = 0
        last_log = start_time

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self._crawl_url, self.start_url): self.start_url}
            while futures:
                for future in as_completed(list(futures)):
                    futures.pop(future, None)
                    result = future.result()
                    processed += 1
                    if result is None:
                        self._log_progress(start_time, processed, last_log)
                        last_log = time.monotonic()
                        continue
                    page, discovered = result
                    if page.markdown.strip():
                        pages.append(page)
                    for url in discovered:
                        if self._mark_visited(url):
                            futures[executor.submit(self._crawl_url, url)] = url
                    self._log_progress(start_time, processed, last_log)
                    last_log = time.monotonic()

        return pages

    def _mark_visited(self, url: str) -> bool:
        with self.lock:
            if url in self.visited:
                return False
            self.visited.add(url)
            return True

    def _log_progress(self, start_time: float, processed: int, last_log: float) -> None:
        now = time.monotonic()
        if now - last_log < 0.5:
            return
        with self.lock:
            discovered = len(self.visited)
        elapsed = max(now - start_time, 0.001)
        rate = processed / elapsed
        remaining = max(discovered - processed, 0)
        eta_seconds = remaining / rate if rate > 0 else 0.0
        print(
            f"Crawled {processed}/{discovered} pages | "
            f"Elapsed {elapsed:.1f}s | ETA {eta_seconds:.1f}s",
            flush=True,
        )

    def _crawl_url(self, url: str) -> tuple[Page, list[str]] | None:
        try:
            response = fetch_url(url)
        except Exception:
            return None
        content = extract_content(
            response.text,
            url,
            self.prefix,
            include_images=self.include_images,
            tag_blacklist=self.tag_blacklist,
            attr_blacklist=self.attr_blacklist,
        )
        page = Page(url=url, title=content.title, markdown=content.markdown, images=content.images)
        return page, content.discovered_urls
