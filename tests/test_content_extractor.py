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
    result = extract_content(
        html,
        base_url="https://example.com/docs/start",
        prefix="https://example.com/docs/",
        tag_blacklist=[],
        attr_blacklist=[],
    )

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
        tag_blacklist=[],
        attr_blacklist=[],
    )

    tokens = [image.token for image in result.images]
    assert len(tokens) == 2
    assert tokens[0] in result.markdown
    assert tokens[1] in result.markdown
    assert result.images[0].url == "https://example.com/images/logo.png"
    assert result.images[1].url == "https://example.com/images/bg.jpg"


def test_extract_content_converts_tables() -> None:
    html = """
    <html>
      <body>
        <table>
          <tr><th>Name</th><th>Value</th></tr>
          <tr><td>One</td><td>1</td></tr>
        </table>
      </body>
    </html>
    """
    result = extract_content(
        html,
        base_url="https://example.com",
        prefix="https://example.com/",
        tag_blacklist=[],
        attr_blacklist=[],
    )

    assert "| Name | Value |" in result.markdown
    assert "| One | 1 |" in result.markdown


def test_tag_blacklist_filters_elements() -> None:
    """Test that tag blacklist filters elements and their content."""
    html = """
    <html>
      <body>
        <p>Visible content</p>
        <nav><p>Navigation content</p></nav>
        <aside><p>Sidebar content</p></aside>
        <p>More visible content</p>
      </body>
    </html>
    """
    result = extract_content(
        html,
        base_url="https://example.com",
        prefix="https://example.com/",
        tag_blacklist=["nav", "aside"],
        attr_blacklist=[],
    )

    assert "Visible content" in result.markdown
    assert "More visible content" in result.markdown
    assert "Navigation content" not in result.markdown
    assert "Sidebar content" not in result.markdown


def test_attr_blacklist_filters_by_class_and_id() -> None:
    """Test that attr blacklist filters elements by class and id."""
    html = """
    <html>
      <body>
        <p>Visible content</p>
        <div class="sidebar-nav"><p>Sidebar content</p></div>
        <div id="footer-section"><p>Footer content</p></div>
        <div class="absolute top-0"><p>Overlay content</p></div>
        <p>More visible content</p>
      </body>
    </html>
    """
    result = extract_content(
        html,
        base_url="https://example.com",
        prefix="https://example.com/",
        tag_blacklist=[],
        attr_blacklist=["sidebar", "footer", "absolute"],
    )

    assert "Visible content" in result.markdown
    assert "More visible content" in result.markdown
    assert "Sidebar content" not in result.markdown
    assert "Footer content" not in result.markdown
    assert "Overlay content" not in result.markdown
