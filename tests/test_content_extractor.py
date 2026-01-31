from mdcrawler.content_extractor import extract_content


def test_extract_content_rewrites_links_and_discovers_internal_urls() -> None:
    html = """
    <html>
      <head><title>Example</title></head>
      <body>
        <p><a href="/docs/page">Internal</a></p>
        <p><a href="https://external.com/page">External</a></p>
      </body>
    </html>
    """
    result = extract_content(html, base_url="https://example.com/docs/start", prefix="https://example.com/docs/")

    assert "Internal" in result.markdown
    assert "[External](https://external.com/page)" in result.markdown
    assert result.discovered_urls == ["https://example.com/docs/page"]


def test_extract_content_includes_images_and_backgrounds() -> None:
    html = """
    <html>
      <body>
        <img src="/images/logo.png" alt="Logo"/>
        <div style="background-image: url('/images/bg.jpg')">Hero</div>
      </body>
    </html>
    """
    result = extract_content(
        html,
        base_url="https://example.com/docs/start",
        prefix="https://example.com/docs/",
        include_images=True,
    )

    tokens = [image.token for image in result.images]
    assert len(tokens) == 2
    assert tokens[0] in result.markdown
    assert tokens[1] in result.markdown
    assert result.images[0].url == "https://example.com/images/logo.png"
    assert result.images[1].url == "https://example.com/images/bg.jpg"
