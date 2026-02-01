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


def test_unordered_and_ordered_lists() -> None:
    """Test that ul uses bullet points and ol uses numbers."""
    html = """
    <html>
      <body>
        <p>Unordered:</p>
        <ul>
          <li>Apple</li>
          <li>Banana</li>
          <li>Cherry</li>
        </ul>
        <p>Ordered:</p>
        <ol>
          <li>First step</li>
          <li>Second step</li>
          <li>Third step</li>
        </ol>
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

    # Unordered list should use bullet points
    assert "- Apple" in result.markdown
    assert "- Banana" in result.markdown
    assert "- Cherry" in result.markdown

    # Ordered list should use numbers
    assert "1. First step" in result.markdown
    assert "2. Second step" in result.markdown
    assert "3. Third step" in result.markdown


def test_list_items_exclude_nested_pre_content() -> None:
    """Test that list items don't include content from nested pre blocks."""
    html = """
    <html>
      <body>
        <ol>
          <li>Create a file:
            <pre><code>SOME_VAR=value</code></pre>
          </li>
          <li>Run the command</li>
        </ol>
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

    # The code block content should appear only once (in the code block)
    assert result.markdown.count("SOME_VAR=value") == 1
    # List item should not contain the code block content
    assert "1. Create a file:" in result.markdown
    assert "1. Create a file: SOME_VAR" not in result.markdown
    # Code block should still be present
    assert "```" in result.markdown


def test_inline_formatting() -> None:
    """Test that em, strong, and code tags are converted to markdown."""
    html = """
    <html>
      <body>
        <p>This is <em>italic</em> and <i>also italic</i> text.</p>
        <p>This is <strong>bold</strong> and <b>also bold</b> text.</p>
        <p>Run <code>npm install</code> to install.</p>
        <p><em>Example:</em> An example here.</p>
        <pre><code>code block should not be affected</code></pre>
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

    # Check italic
    assert "*italic*" in result.markdown
    assert "*also italic*" in result.markdown

    # Check bold
    assert "**bold**" in result.markdown
    assert "**also bold**" in result.markdown

    # Check inline code
    assert "`npm install`" in result.markdown

    # Check combined
    assert "*Example:*" in result.markdown

    # Code blocks should still work (no backticks inside)
    assert "```" in result.markdown
    assert "code block should not be affected" in result.markdown


def test_images_in_picture_elements_appear_at_correct_position() -> None:
    """Test that images inside picture/span/div wrappers appear at correct position."""
    html = """
    <html>
      <body>
        <p>First paragraph.</p>
        <div class="frame">
          <span>
            <picture class="contents">
              <img src="/images/screenshot.png" alt="Screenshot"/>
            </picture>
          </span>
        </div>
        <p>Second paragraph.</p>
      </body>
    </html>
    """
    result = extract_content(
        html,
        base_url="https://example.com",
        prefix="https://example.com/",
        include_images=True,
        tag_blacklist=[],
        attr_blacklist=[],
    )

    # Image token should be present
    assert len(result.images) == 1
    assert result.images[0].token in result.markdown

    # Image should appear between the two paragraphs
    first_para_pos = result.markdown.find("First paragraph.")
    image_pos = result.markdown.find(result.images[0].token)
    second_para_pos = result.markdown.find("Second paragraph.")
    assert (
        first_para_pos < image_pos < second_para_pos
    ), "Image should appear between the two paragraphs"
