from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable

import requests


def fetch_urls(urls: Iterable[str], max_workers: int) -> list[tuple[str, requests.Response | None]]:
    results: list[tuple[str, requests.Response | None]] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(_fetch, url): url for url in urls}
        for future in as_completed(future_map):
            url = future_map[future]
            try:
                response = future.result()
            except requests.RequestException:
                response = None
            results.append((url, response))
    return results


def fetch_url(url: str) -> requests.Response:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response


def _fetch(url: str) -> requests.Response:
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response
