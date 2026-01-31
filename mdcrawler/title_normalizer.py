from __future__ import annotations

from collections import Counter
from typing import Iterable

SEPARATORS = [" - ", " | ", " – "]


def normalize_titles(titles: Iterable[str]) -> list[str]:
    titles_list = list(titles)
    if not titles_list:
        return []

    prefix, suffix = _infer_common_affixes(titles_list)
    return [_strip_affixes(title, prefix, suffix) for title in titles_list]


def _infer_common_affixes(titles: list[str]) -> tuple[str | None, str | None]:
    prefix_counter: Counter[str] = Counter()
    suffix_counter: Counter[str] = Counter()

    for title in titles:
        parts = _split_title(title)
        if parts:
            prefix_counter[parts[0]] += 1
            suffix_counter[parts[-1]] += 1

    min_count = max(2, len(titles) // 2)
    prefix = _most_common(prefix_counter, min_count)
    suffix = _most_common(suffix_counter, min_count)
    return prefix, suffix


def _split_title(title: str) -> list[str]:
    for sep in SEPARATORS:
        if sep in title:
            return [part.strip() for part in title.split(sep) if part.strip()]
    return [title.strip()]


def _most_common(counter: Counter[str], min_count: int) -> str | None:
    if not counter:
        return None
    candidate, count = counter.most_common(1)[0]
    if count >= min_count:
        return candidate
    return None


def _strip_affixes(title: str, prefix: str | None, suffix: str | None) -> str:
    cleaned = title
    if prefix and cleaned.startswith(prefix):
        cleaned = cleaned[len(prefix) :].lstrip(" -|–")
    if suffix and cleaned.endswith(suffix):
        cleaned = cleaned[: -len(suffix)].rstrip(" -|–")
    return cleaned.strip() or title
