import requests

from mdcrawler.content_extractor import extract_content


def test_app_code_introduction_contains_expected_strings() -> None:
    url = "https://docs.base44.com/developers/app-code/overview/introduction"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    result = extract_content(
        response.text,
        base_url=url,
        prefix="https://docs.base44.com/developers/",
        blacklist=["navigation", "sidebar", "contents", "toolbar", "pagination", "footer"],
    )
    markdown = result.markdown
    normalized = " ".join(markdown.split())

    assert (
        "Take full control of your Base44 apps with direct code access. Edit code directly, debug API calls, "
        "and integrate with GitHub while keeping AI assistance available when you need it."
        in markdown
    )
    assert "Build and edit Base44 apps with AI assistance and developer tools." in markdown
    assert "Base44 apps use a modern frontend stack with a fully managed backend:" in markdown
    assert "# Frontend" in markdown
    assert "# Base44 SDK" in markdown
    assert (
        "Your interface to all Base44 backend services. Use it in your frontend components or backend functions "
        "to access data, auth, integrations, and more."
        in markdown
    )
    assert "to explore and edit your app’s source code." in markdown
    assert "Search..." not in markdown
    assert "Ask AI" not in markdown
    assert "On this page" not in markdown
    assert "Was this page helpful?" not in markdown
    assert "discord" not in markdown.lower()
    assert "Powered by" not in markdown
    assert "Project Structure" not in markdown
    assert "⌘ I" not in markdown


def test_code_tab_page_contains_expected_strings() -> None:
    url = "https://docs.base44.com/developers/app-code/editor/code-tab"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    result = extract_content(
        response.text,
        base_url=url,
        prefix="https://docs.base44.com/developers/",
        blacklist=["navigation", "sidebar", "contents", "toolbar", "pagination", "footer"],
    )
    markdown = result.markdown
    normalized = " ".join(markdown.split())

    assert "Can I edit every part of my app's code?" in markdown
    assert (
        "Yes. You can open and edit any code file that appears in the Code files "
        "panel, including pages, components, layouts, and entity helpers. If a part "
        "of the app is generated for you, it still appears as regular code that you "
        "can modify."
        in normalized
    )
