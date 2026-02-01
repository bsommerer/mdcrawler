from __future__ import annotations

from dataclasses import dataclass
import re
from urllib.parse import urljoin, urlsplit, urlunsplit

from bs4 import BeautifulSoup
from bs4.element import Tag


# Pre-compiled regex patterns
_ID_SPLIT_PATTERN = re.compile(r"[^a-zA-Z0-9]+")
_URL_PATTERN = re.compile(r"url\((?P<quote>['\"]?)(?P<url>[^)'\"]+)(?P=quote)\)")


# Default blacklists
DEFAULT_TAG_BLACKLIST = [
    "nav",
    "aside",
    "footer",
    "form",
    "button",
    "input",
    "textarea",
    "select",
    "noscript",
    "script",
    "style",
    "svg",
    "iframe",
]

DEFAULT_ATTR_BLACKLIST = [
    "navigation",
    "sidebar",
    "contents",
    "toolbar",
    "pagination",
    "footer",
    "absolute",
]


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


def extract_content(
    html: str,
    base_url: str,
    prefix: str,
    include_images: bool = False,
    tag_blacklist: list[str] | None = None,
    attr_blacklist: list[str] | None = None,
) -> ExtractedContent:
    soup = BeautifulSoup(html, "html.parser")
    images: list[ImageReference] = []

    # Use defaults if not provided
    tag_bl = set(t.lower() for t in (tag_blacklist if tag_blacklist is not None else DEFAULT_TAG_BLACKLIST))
    attr_bl = [item.lower() for item in (attr_blacklist if attr_blacklist is not None else DEFAULT_ATTR_BLACKLIST)]

    if include_images:
        images = _extract_images(soup, base_url)
    _promote_data_as_tags(soup)
    _strip_blacklisted(soup, tag_bl, attr_bl)
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

    content_roots = _content_roots(soup)
    markdown = _html_to_markdown(soup, content_roots)
    return ExtractedContent(
        title=title,
        markdown=markdown,
        discovered_urls=discovered_urls,
        images=images,
    )


def _strip_blacklisted(soup: BeautifulSoup, tag_blacklist: set[str], attr_blacklist: list[str]) -> None:
    """Remove blacklisted elements from the DOM in a single traversal."""
    # Collect elements to remove (can't modify while iterating)
    to_remove: list[Tag] = []
    for tag in soup.find_all(True):
        if not isinstance(tag, Tag):
            continue
        # Check tag blacklist
        if tag.name in tag_blacklist:
            to_remove.append(tag)
            continue
        # Check attribute blacklist
        if attr_blacklist and _matches_attr_blacklist(tag, attr_blacklist):
            to_remove.append(tag)

    # Remove collected elements
    for tag in to_remove:
        tag.decompose()


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

    for tag in soup.find_all(True):
        if not isinstance(tag, Tag) or tag.attrs is None:
            continue
        style = tag.get("style", "")
        if "background-image" not in style:
            continue
        for match in _URL_PATTERN.finditer(style):
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


def _html_to_markdown(soup: BeautifulSoup, content_roots: list[Tag]) -> str:
    """Convert HTML to markdown. Blacklisted elements are already stripped from DOM."""
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
        "details",
        "summary",
    }
    lines: list[str] = []
    body = soup.body or soup
    for element in body.find_all(block_tags):
        if element.find_parent("details") is not None and element.name != "details":
            continue
        if element.name in {"div", "header", "section"} and _has_block_child(element, block_tags):
            continue
        if content_roots and not _is_within_roots(element, content_roots):
            continue
        if element.name == "summary":
            continue
        text = element.get_text(" ", strip=True)
        if not text:
            continue
        if element.name == "details":
            lines.extend(_details_to_markdown(element))
            lines.append("")
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


def _matches_attr_blacklist(element: Tag, attr_blacklist: list[str]) -> bool:
    """Check if element's class or id matches any blacklisted term."""
    if not attr_blacklist or element.attrs is None:
        return False

    # Check class attribute
    class_tokens = [token.lower() for token in element.get("class", [])]
    for token in class_tokens:
        sub_tokens = {token}
        for part in token.replace("_", "-").split("-"):
            if part:
                sub_tokens.add(part)
        if any(term in sub_tokens for term in attr_blacklist):
            return True

    # Check id attribute
    tag_id = element.get("id", "")
    if tag_id:
        id_tokens = _ID_SPLIT_PATTERN.split(tag_id.lower())
        if any(term in id_tokens for term in attr_blacklist):
            return True

    return False


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


def _details_to_markdown(details: Tag) -> list[str]:
    lines: list[str] = []
    summary = details.find("summary")
    summary_text = summary.get_text(" ", strip=True) if summary else ""
    if summary_text:
        lines.append(f"## {summary_text}")
    body_texts: list[str] = []
    for child in details.find_all(True, recursive=False):
        if child is summary:
            continue
        text = child.get_text(" ", strip=True)
        if text:
            body_texts.append(text)
    if body_texts:
        lines.append(" ".join(body_texts))
    return lines


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


def _content_roots(soup: BeautifulSoup) -> list[Tag]:
    roots: list[Tag] = []
    for tag_name in ("main", "article"):
        for tag in soup.find_all(tag_name):
            roots.append(tag)
    for tag in soup.find_all(attrs={"data-page-title": True}):
        roots.append(tag)
    for tag in soup.find_all(id=True):
        tag_id = tag.get("id", "").lower()
        if "content" in tag_id:
            roots.append(tag)
    return roots


def _is_within_roots(element: Tag, roots: list[Tag]) -> bool:
    for parent in element.parents:
        if parent in roots:
            return True
    return False
