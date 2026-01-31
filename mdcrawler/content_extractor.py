from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup
from bs4.element import Tag


@dataclass
class ExtractedContent:
    title: str
    markdown: str
    discovered_urls: list[str]


def extract_content(html: str, base_url: str, prefix: str) -> ExtractedContent:
    soup = BeautifulSoup(html, "html.parser")
    _strip_layout(soup)

    discovered_urls: list[str] = []
    for link in soup.find_all("a", href=True):
        href = link.get("href", "")
        absolute = urljoin(base_url, href)
        normalized = _normalize_url(absolute)
        text = link.get_text(strip=True) or normalized
        if not normalized:
            link.replace_with(text)
            continue
        if normalized.startswith(prefix):
            discovered_urls.append(normalized)
            link.replace_with(text)
        else:
            link.replace_with(f"[{text}]({normalized})")

    title_tag = soup.find("title")
    title = title_tag.get_text(strip=True) if title_tag else base_url

    markdown = _html_to_markdown(soup)
    return ExtractedContent(title=title, markdown=markdown, discovered_urls=discovered_urls)


def _strip_layout(soup: BeautifulSoup) -> None:
    for tag_name in ["img", "header", "footer", "nav", "aside"]:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    for tag in soup.find_all(True):
        if not isinstance(tag, Tag) or tag.attrs is None:
            continue
        classes = " ".join(tag.get("class", []))
        tag_id = tag.get("id", "")
        if "sidebar" in classes or "sidebar" in tag_id:
            tag.decompose()


def _normalize_url(url: str) -> str:
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"}:
        return ""
    path = parts.path or "/"
    return urlunsplit((parts.scheme, parts.netloc, path, parts.query, ""))


def _html_to_markdown(soup: BeautifulSoup) -> str:
    lines: list[str] = []
    body = soup.body or soup
    for element in body.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "pre"]):
        text = element.get_text(" ", strip=True)
        if not text:
            continue
        if element.name.startswith("h"):
            level = int(element.name[1])
            lines.append(f"{'#' * level} {text}")
        elif element.name == "li":
            lines.append(f"- {text}")
        elif element.name == "pre":
            lines.append("```")
            lines.append(text)
            lines.append("```")
        else:
            lines.append(text)
        lines.append("")
    return "\n".join(lines).strip() + "\n"
