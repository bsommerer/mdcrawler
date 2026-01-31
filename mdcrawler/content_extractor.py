from __future__ import annotations

from dataclasses import dataclass
import re
from urllib.parse import urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup
from bs4.element import Tag


@dataclass
class ExtractedContent:
    title: str
    markdown: str
    discovered_urls: list[str]
    images: list["ImageReference"]


@dataclass
class ImageReference:
    token: str
    url: str
    alt: str
    filename: str | None = None


def extract_content(html: str, base_url: str, prefix: str, include_images: bool = False) -> ExtractedContent:
    soup = BeautifulSoup(html, "html.parser")
    images: list[ImageReference] = []
    if include_images:
        images = _extract_images(soup, base_url)
    _promote_data_as_tags(soup)
    _strip_layout(soup, include_images=include_images)
    _replace_tables(soup)

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
    return ExtractedContent(
        title=title,
        markdown=markdown,
        discovered_urls=discovered_urls,
        images=images,
    )


def _strip_layout(soup: BeautifulSoup, include_images: bool) -> None:
    if not include_images:
        for tag in soup.find_all("img"):
            tag.decompose()


def _extract_images(soup: BeautifulSoup, base_url: str) -> list[ImageReference]:
    images: list[ImageReference] = []

    for image in soup.find_all("img", src=True):
        src = image.get("src", "")
        absolute = urljoin(base_url, src)
        normalized = _normalize_url(absolute)
        if not normalized:
            continue
        alt_text = image.get("alt", "").strip()
        token = f"[[IMAGE_{len(images)}]]"
        images.append(ImageReference(token=token, url=normalized, alt=alt_text))
        placeholder = soup.new_tag("p")
        placeholder.string = token
        image.replace_with(placeholder)

    url_pattern = re.compile(r"url\((?P<quote>['\"]?)(?P<url>[^)'\"]+)(?P=quote)\)")
    for tag in soup.find_all(True):
        if not isinstance(tag, Tag) or tag.attrs is None:
            continue
        style = tag.get("style", "")
        if "background-image" not in style:
            continue
        for match in url_pattern.finditer(style):
            candidate = match.group("url")
            absolute = urljoin(base_url, candidate)
            normalized = _normalize_url(absolute)
            if not normalized:
                continue
            token = f"[[IMAGE_{len(images)}]]"
            images.append(ImageReference(token=token, url=normalized, alt=""))
            placeholder = soup.new_tag("p")
            placeholder.string = token
            tag.insert_after(placeholder)

    return images


def _replace_tables(soup: BeautifulSoup) -> None:
    for table in soup.find_all("table"):
        markdown = _table_to_markdown(table)
        placeholder = soup.new_tag("p")
        placeholder.string = markdown
        table.replace_with(placeholder)


def _normalize_url(url: str) -> str:
    parts = urlsplit(url)
    if parts.scheme not in {"http", "https"}:
        return ""
    path = parts.path or "/"
    return urlunsplit((parts.scheme, parts.netloc, path, parts.query, ""))


def _html_to_markdown(soup: BeautifulSoup) -> str:
    block_tags = {
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "p",
        "li",
        "pre",
        "table",
        "div",
        "header",
        "section",
    }
    lines: list[str] = []
    body = soup.body or soup
    for element in body.find_all(block_tags):
        if element.name in {"div", "header", "section"} and _has_block_child(element, block_tags):
            continue
        text = element.get_text(" ", strip=True)
        if not text:
            continue
        if element.name == "p" and _is_strong_only(element):
            lines.append(f"# {text}")
        elif element.name.startswith("h"):
            level = int(element.name[1])
            lines.append(f"{'#' * level} {text}")
        elif element.name == "table":
            lines.extend(text.splitlines())
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


def _is_strong_only(element: Tag) -> bool:
    children = [child for child in element.find_all(True, recursive=False)]
    if len(children) != 1 or children[0].name != "strong":
        return False
    return element.get_text(" ", strip=True) == children[0].get_text(" ", strip=True)


def _has_block_child(element: Tag, block_tags: set[str]) -> bool:
    for child in element.find_all(True):
        if child is element:
            continue
        if child.name in block_tags and child.name not in {"div", "header", "section"}:
            return True
    return False


def _table_to_markdown(table: Tag) -> str:
    rows = []
    for row in table.find_all("tr"):
        cells = [cell.get_text(" ", strip=True) for cell in row.find_all(["th", "td"])]
        if cells:
            rows.append(cells)
    if not rows:
        return ""
    header = rows[0]
    body_rows = rows[1:] if len(rows) > 1 else []
    column_count = max(len(header), max((len(row) for row in body_rows), default=0))
    header = header + [""] * (column_count - len(header))
    lines = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * column_count) + " |"]
    for row in body_rows:
        row = row + [""] * (column_count - len(row))
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def _promote_data_as_tags(soup: BeautifulSoup) -> None:
    allowed = {
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "li",
        "pre",
    }
    for tag in soup.find_all(attrs={"data-as": True}):
        if not isinstance(tag, Tag):
            continue
        value = tag.get("data-as", "").strip().lower()
        if value in allowed:
            tag.name = value
