import requests

from mdcrawler.content_extractor import extract_content


def test_app_code_introduction_contains_expected_strings() -> None:
    url = "https://docs.base44.com/developers/app-code/overview/introduction"
    response = requests.get(url, timeout=30)
    response.raise_for_status()

    result = extract_content(response.text, base_url=url, prefix="https://docs.base44.com/developers/")
    markdown = result.markdown

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
